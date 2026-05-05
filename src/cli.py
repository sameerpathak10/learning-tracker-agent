import sys
import logging
from agent import create_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    print("Initializing Learning Tracker Agent (AWS Agentcore Memory POC)...")
    try:
        agent = create_agent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        print("Please ensure AWS credentials are set and 'strands-agents' is installed.")
        sys.exit(1)
        
    print("\nAgent ready! Type 'exit' to quit.")
    print("Example: 'I am learning Kubernetes. I just finished Pods.'")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ['exit', 'quit']:
                break
            
            # The agent maintains STM (Short Term Memory) automatically across the session
            # Strands SDK handles the conversation history natively within the Agent instance
            response = agent(user_input)
            print(f"\nAgent: {response}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
