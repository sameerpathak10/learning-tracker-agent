from strands import Agent
from tools import update_learning_progress, get_learning_progress, update_preferences, get_preferences

def create_agent():
    """
    Creates and configures the Learning Tracker Agent using the Strands SDK.
    """
    system_prompt = (
        "You are a helpful Learning Tracker Agent. Your job is to help the user "
        "track their learning progress, remember their preferences (like videos vs docs, pace), "
        "and help them pick up exactly where they left off in their next session.\n"
        "Always use your tools to update or retrieve their progress and preferences.\n"
        "If you see preferences, try to suggest learning materials that match them."
    )
    
    agent = Agent(
        system_prompt=system_prompt,
        tools=[
            update_learning_progress, 
            get_learning_progress, 
            update_preferences, 
            get_preferences
        ],
        # Amazon Bedrock is the default model provider for Strands Agents
    )
    
    return agent
