import uuid
import logging
from boto3.session import Session
from bedrock_agentcore_starter_toolkit.operations.memory.manager import MemoryManager
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.constants import StrategyType
from learning_tracker_agent.config import REGION

logger = logging.getLogger(__name__)

MEMORY_NAME = "LearningTrackerMemory"
ACTOR_ID = "learner_001"


def create_or_get_memory():
    memory_manager = MemoryManager(region_name=REGION)
    memory = memory_manager.get_or_create_memory(
        name=MEMORY_NAME,
        strategies=[
            {
                StrategyType.USER_PREFERENCE.value: {
                    "name": "LearnerPreferences",
                    "description": "Captures learner preferences and learning style",
                    "namespaces": ["learning/learner/{actorId}/preferences/"],
                }
            },
            {
                StrategyType.SEMANTIC.value: {
                    "name": "LearningProgress",
                    "description": "Stores topics learned, progress, and concepts covered",
                    "namespaces": ["learning/learner/{actorId}/progress/"],
                }
            },
        ],
    )
    memory_id = memory["id"]
    print(f"Memory ready: {memory_id}")
    return memory_id


def seed_memory(memory_id: str):
    memory_client = MemoryClient(region_name=REGION)
    previous_interactions = [
        ("I'm learning Kubernetes. What have I covered so far?", "USER"),
        (
            "Based on your learning journey in Kubernetes, you've covered Pods and Services. Let me help you track more progress.",
            "ASSISTANT",
        ),
        ("I've studied Pods and Services today. That took 3 hours.", "USER"),
        (
            "Great! Progress recorded. You've covered Pods and Services in Kubernetes (3 hours). The next topics to cover are Deployments and StatefulSets.",
            "ASSISTANT",
        ),
        ("I prefer learning through videos. What's my learning pace?", "USER"),
        (
            "Your preferences show you like video-based content. I'll prioritize video tutorials for Deployments and StatefulSets next.",
            "ASSISTANT",
        ),
        ("I completed Deployments yesterday. About 2 hours.", "USER"),
        (
            "Excellent! Deployments completed (2 hours). You're making steady progress. Next is StatefulSets, which is crucial for Kubernetes.",
            "ASSISTANT",
        ),
        ("What topics should I learn next after Kubernetes?", "USER"),
        (
            "Based on your DevOps learning path and video preference, I recommend Docker next as a foundation, followed by Terraform for Infrastructure as Code.",
            "ASSISTANT",
        ),
    ]

    memory_client.create_event(
        memory_id=memory_id,
        actor_id=ACTOR_ID,
        session_id="previous_session",
        messages=previous_interactions,
    )
    print("Seeded learning history successfully")


if __name__ == "__main__":
    memory_id = create_or_get_memory()
    seed_memory(memory_id)
    print("Memory setup complete.")
