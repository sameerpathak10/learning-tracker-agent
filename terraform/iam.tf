data "aws_caller_identity" "current" {}

resource "aws_iam_role" "agent_role" {
  name = "${var.agent_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "agent_bedrock_policy" {
  name        = "${var.agent_name}-bedrock-policy"
  description = "Allows the agent to invoke Bedrock models and use Agentcore Memory"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:CreateSession",
          "bedrock:GetSession",
          "bedrock:UpdateSession",
          "bedrock:DeleteSession",
          "bedrock:CreateInvocationStep"
        ]
        Resource = "arn:aws:bedrock:${var.aws_region}:${data.aws_caller_identity.current.account_id}:session/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "agent_bedrock_attach" {
  role       = aws_iam_role.agent_role.name
  policy_arn = aws_iam_policy.agent_bedrock_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.agent_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
