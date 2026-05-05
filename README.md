# Learning Tracker Agent POC

This project implements a Proof of Concept (POC) for a Learning Tracker Agent using the [Strands SDK](https://strandsagents.com/), AWS Agentcore Memory, and Terraform.

## Prerequisites

- Python 3.10+
- AWS CLI installed and configured
- Terraform installed

## Setup Instructions

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Local Testing CLI:**
   You must have valid AWS credentials in your environment.
   ```bash
   python src/cli.py
   ```

3. **Deploy with Terraform:**
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

## Architecture
- `src/agent.py`: Agent initialization using Strands SDK.
- `src/tools.py`: Tools for Long-Term Memory (progress and preferences).
- `src/memory.py`: Wrappers for AWS Agentcore Memory API.
- `src/cli.py`: Command line interface.
- `terraform/`: Infrastructure to set up permissions and resources for Agentcore.
