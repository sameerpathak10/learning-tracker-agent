import uuid
from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

from .config import MODEL_ID, MEMORY_ID, ACTOR_ID, REGION, SYSTEM_PROMPT
from .tools import (
    add_topic,
    record_progress,
    get_learning_status,
    get_topic_recommendations,
    update_learning_preference,
)
from .memory_hooks import LearningTrackerMemoryHooks


def get_learning_tracker_agent(session_id: str = None) -> Agent:
    if session_id is None:
        session_id = str(uuid.uuid4())

    memory_client = MemoryClient(region_name=REGION)
    memory_hooks = LearningTrackerMemoryHooks(
        memory_id=MEMORY_ID,
        client=memory_client,
        actor_id=ACTOR_ID,
        session_id=session_id,
    )

    memory_config = AgentCoreMemoryConfig(
        memory_id=MEMORY_ID,
        session_id=session_id,
        actor_id=ACTOR_ID,
        retrieval_config={
            "learning/learner/{actorId}/progress/": RetrievalConfig(top_k=3, relevance_score=0.2),
            "learning/learner/{actorId}/preferences/": RetrievalConfig(top_k=3, relevance_score=0.2),
        },
    )

    model = BedrockModel(model_id=MODEL_ID, region_name=REGION)

    return Agent(
        model=model,
        session_manager=AgentCoreMemorySessionManager(memory_config, REGION),
        system_prompt=SYSTEM_PROMPT,
        tools=[
            add_topic,
            record_progress,
            get_learning_status,
            get_topic_recommendations,
            update_learning_preference,
        ],
        hooks=[memory_hooks],
    )
