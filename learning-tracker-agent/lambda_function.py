import json
from learning_tracker_agent.agent_builder import get_learning_tracker_agent


def lambda_handler(event, context):
    query = None
    if isinstance(event, dict):
        query = event.get("query") or event.get("body")
        if isinstance(query, str) and event.get("isBase64Encoded"):
            query = query

    if not query:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'query' in event payload."}),
        }

    agent = get_learning_tracker_agent()
    try:
        response = agent(query)
        return {
            "statusCode": 200,
            "body": json.dumps({"result": response}),
        }
    except Exception as exc:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(exc)}),
        }
