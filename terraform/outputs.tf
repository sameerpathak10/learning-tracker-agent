output "agent_role_arn" {
  value = aws_iam_role.agent_role.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.agent_lambda.function_name
}
