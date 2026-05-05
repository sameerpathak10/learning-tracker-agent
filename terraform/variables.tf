variable "aws_region" {
  description = "The AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "agent_name" {
  description = "Name of the learning tracker agent"
  type        = string
  default     = "learning-tracker-agent"
}
