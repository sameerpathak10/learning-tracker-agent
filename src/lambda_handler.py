import json
from agent import create_agent

def lambda_handler(event, context):
    """
    AWS Lambda entry point for the Learning Tracker Agent.
    """
    try:
        agent = create_agent()
        
        # Parse user input from event body
        body = json.loads(event.get("body", "{}"))
        user_input = body.get("input", "")
        
        if not user_input:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No input provided"})
            }
            
        # Invoke agent
        response = agent(user_input)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"response": response})
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
