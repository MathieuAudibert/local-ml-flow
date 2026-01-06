variable "endpoint" {
  type    = string
  default = "http://localhost:4566"
}

variable "access_key" {
  type = string
}

variable "secret_key" {
  type = string
}

variable "region" {
  type = string
}

provider "aws" {
  access_key                  = var.access_key
  secret_key                  = var.secret_key
  region                      = var.region
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3     = var.endpoint
    lambda = var.endpoint
    iam    = var.endpoint
  }
}

resource "aws_s3_bucket" "ml_data" {
  bucket = "local-ml-flow-data"
}

resource "aws_s3_bucket" "ml_models" {
  bucket = "local-ml-flow-models"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" } }]
  })
}

resource "aws_lambda_layer_version" "ml_libs" {
  filename   = "ml_layer.zip"
  layer_name = "ml_features_layer"

  compatible_runtimes = ["python3.10"]
}

resource "aws_lambda_function" "ingestion" {
  filename      = "ingestion.zip"
  function_name = "local-ml-flow-ingestion"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "src.core.lambdas.ingestion.handler"
  runtime       = "python3.10"
  layers        = [aws_lambda_layer_version.ml_libs.arn]
  environment {
    variables = {
      PYTHONPATH   = "/var/task"
      endpoint_url = var.endpoint
    }
  }
}

resource "aws_lambda_function" "inference" {
  filename      = "inference.zip"
  function_name = "local-ml-flow-inference"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "src.core.lambdas.inference.handler"
  runtime       = "python3.10"
  layers        = [aws_lambda_layer_version.ml_libs.arn]
  environment {
    variables = {
      PYTHONPATH   = "/var/task"
      endpoint_url = var.endpoint
    }
  }
}
