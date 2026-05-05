from strands import tool
from memory import AgentcoreMemoryWrapper

# Global memory instance for POC (representing a single user session)
memory_wrapper = AgentcoreMemoryWrapper(user_id="default_user")

@tool
def update_learning_progress(topic: str, status: str) -> str:
    """
    Updates the user's learning progress for a specific topic.
    Use this when the user says they have learned or studied something new.
    status should be a brief description, e.g. "Completed", "In Progress", "Just started".
    """
    success = memory_wrapper.save_progress(topic, status)
    if success:
        return f"Successfully updated progress for '{topic}' to '{status}'."
    return "Failed to update progress."

@tool
def get_learning_progress() -> str:
    """
    Retrieves the user's current learning progress across all topics.
    Use this when the user asks what they have covered so far, or where they left off.
    """
    progress = memory_wrapper.get_all_progress()
    if not progress:
        return "You have not started any topics yet."
    
    report = "Here is your learning progress:\n"
    for topic, status in progress.items():
        report += f"- {topic}: {status}\n"
    return report

@tool
def update_preferences(videos_preferred: bool, preferred_pace: str) -> str:
    """
    Updates the user's learning preferences.
    Use this when the user mentions how they like to learn (e.g. videos vs docs) or their pace.
    """
    prefs = {
        "videos_preferred": videos_preferred,
        "preferred_pace": preferred_pace
    }
    success = memory_wrapper.save_preferences(prefs)
    if success:
        return "Successfully updated learning preferences."
    return "Failed to update learning preferences."

@tool
def get_preferences() -> str:
    """
    Retrieves the user's learning preferences.
    Use this to tailor your response based on whether they like videos or docs, and their pace.
    """
    prefs = memory_wrapper.get_preferences()
    if not prefs:
        return "No specific learning preferences recorded."
    return str(prefs)
