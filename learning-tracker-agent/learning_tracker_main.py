from learning_tracker_agent.agent_builder import get_learning_tracker_agent
from learning_tracker_agent.config import REGION

if __name__ == "__main__":
    agent = get_learning_tracker_agent()

    print("\n📚 Learning Tracker Agent Started")
    print("Type 'exit' to quit.\n")
    print("Example queries:")
    print("  'I'm learning Kubernetes. What have I covered so far?'")
    print("  'Record: I studied Pods and Services today, 3 hours'")
    print("  'What should I learn next?'\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Exiting Learning Tracker Agent...")
            break
        try:
            response = agent(user_input)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
