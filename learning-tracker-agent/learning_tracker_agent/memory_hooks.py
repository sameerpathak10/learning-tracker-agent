import logging
from bedrock_agentcore.memory import MemoryClient
from strands.hooks import AfterInvocationEvent, HookProvider, HookRegistry, MessageAddedEvent

logger = logging.getLogger(__name__)

class LearningTrackerMemoryHooks(HookProvider):
    """Memory hooks for learning tracker agent"""

    def __init__(self, memory_id: str, client: MemoryClient, actor_id: str, session_id: str):
        self.memory_id = memory_id
        self.client = client
        self.actor_id = actor_id
        self.session_id = session_id
        self.namespaces = {
            i["type"]: i["namespaces"][0]
            for i in self.client.get_memory_strategies(self.memory_id)
        }

    def retrieve_learning_context(self, event: MessageAddedEvent):
        messages = event.agent.messages
        if messages[-1]["role"] == "user" and "toolResult" not in messages[-1]["content"][0]:
            user_query = messages[-1]["content"][0]["text"]
            try:
                all_context = []
                for context_type, namespace in self.namespaces.items():
                    memories = self.client.retrieve_memories(
                        memory_id=self.memory_id,
                        namespace=namespace.format(actorId=self.actor_id),
                        query=user_query,
                        top_k=3,
                    )
                    for memory in memories:
                        if isinstance(memory, dict):
                            content = memory.get("content", {})
                            if isinstance(content, dict):
                                text = content.get("text", "").strip()
                                if text:
                                    all_context.append(f"[{context_type.upper()}] {text}")
                if all_context:
                    context_text = "\n".join(all_context)
                    original_text = messages[-1]["content"][0]["text"]
                    messages[-1]["content"][0]["text"] = (
                        f"Learning Context:\n{context_text}\n\n{original_text}"
                    )
                    logger.info(f"Retrieved {len(all_context)} learning context items")
            except Exception as e:
                logger.error(f"Failed to retrieve learning context: {e}")

    def save_learning_interaction(self, event: AfterInvocationEvent):
        try:
            messages = event.agent.messages
            if len(messages) >= 2 and messages[-1]["role"] == "assistant":
                learner_query = None
                agent_response = None
                for msg in reversed(messages):
                    if msg["role"] == "assistant" and not agent_response:
                        agent_response = msg["content"][0]["text"]
                    elif msg["role"] == "user" and not learner_query and "toolResult" not in msg["content"][0]:
                        learner_query = msg["content"][0]["text"]
                        break
                if learner_query and agent_response:
                    self.client.create_event(
                        memory_id=self.memory_id,
                        actor_id=self.actor_id,
                        session_id=self.session_id,
                        messages=[(learner_query, "USER"), (agent_response, "ASSISTANT")],
                    )
                    logger.info("Saved learning interaction to memory")
        except Exception as e:
            logger.error(f"Failed to save learning interaction: {e}")

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(MessageAddedEvent, self.retrieve_learning_context)
        registry.add_callback(AfterInvocationEvent, self.save_learning_interaction)
        logger.info("Learning tracker memory hooks registered")
