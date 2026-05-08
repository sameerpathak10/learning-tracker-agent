# Learning Tracker Agent

This repository contains a Learning Tracker Agent designed for AWS code zip deployment. The agent uses AgentCore memory to track:
- learning topics and progress
- learner preferences (video vs docs and pace)
- short-term session dialogue and long-term learning history

## Structure

- `learning_tracker_agent/` - Python package with agent modules
- `lambda_function.py` - AWS Lambda entry point
- `requirements.txt` - Python dependencies
- `learning_tracker_main.py` - CLI runner for local testing

## Deployment

1. Set `MEMORY_ID` environment variable or update `learning_tracker_agent/config.py`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Initialize memory and seed sample learning history:
```bash
python memory_setup.py
```
4. Zip the package contents for Lambda deployment.

## Local Test

Run:
```bash
python learning_tracker_main.py
```

## Lambda Event Format

```json
{
  "query": "I'm learning Kubernetes. What have I covered so far?"
}
```
