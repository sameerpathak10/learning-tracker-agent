data "archive_file" "agent_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/agent.zip"
}

resource "aws_lambda_function" "agent_lambda" {
  filename         = data.archive_file.agent_zip.output_path
  function_name    = var.agent_name
  role             = aws_iam_role.agent_role.arn
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.10"
  timeout          = 60
  
  source_code_hash = data.archive_file.agent_zip.output_base64sha256

  environment {
    variables = {
      REGION = var.aws_region
    }
  }
}
