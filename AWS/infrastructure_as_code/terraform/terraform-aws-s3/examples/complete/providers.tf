# This providers file is configured to deploy the complete
# example in the sandbox account
terraform {
  required_version = "~> 1.0"
  required_providers {
    aws = {
      source  = "aws"
      version = "~> 3"
    }
  }
}

provider "aws" {
  region              = "us-east-1"
  allowed_account_ids = ["658350424896"]
}
