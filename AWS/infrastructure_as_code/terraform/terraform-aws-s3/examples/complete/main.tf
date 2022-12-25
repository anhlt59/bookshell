# In this example, we should enable all optional configurations
# to ensure the configuration is fully applied in the test
# environment

variable "deployment_id" {
  description = "unique identifier for this deployment"
  type        = string
}

# Default will only place a lifecycle policy on noncurrent objects
module "this_default" {
  source         = "../../"
  bucket_name    = "${var.deployment_id}-s3-ci-test"
  force_destroy  = true
  enable_metrics = true
}

module "this_with_30_day" {
  source                       = "../../"
  bucket_name                  = "${var.deployment_id}-30-day-s3-ci-test"
  force_destroy                = true
  lifecycle_policy_enforcement = "delete_everything_after_30_days"
}

module "this_with_specified_retention" {
  source                       = "../../"
  bucket_name                  = "${var.deployment_id}-retention-s3-ci-test"
  force_destroy                = true
  lifecycle_policy_enforcement = "delete_everything_after_n_days"

  retention_days = 7
}

module "this_with_custom_days" {
  source        = "../../"
  bucket_name   = "${var.deployment_id}-custom-s3-ci-test"
  force_destroy = true

  # choose custom lifecylcle and pass in the below values
  lifecycle_policy_enforcement = "custom"

  # main bucket
  custom_domain_main_lifecycle = {
    noncurrent_ia_days        = 30
    noncurrent_glacier_days   = 60
    noncurrent_retention_days = 90
    regular_ia_days           = 31
    regular_glacier_days      = 61
    regular_retention_days    = 91
  }

  # access log bucket
  custom_domain_access_logs_lifecycle = {
    regular_ia_days        = 33
    regular_glacier_days   = 63
    regular_retention_days = 93
  }
}

module "this_with_30_day_and_cors" {
  source                       = "../../"
  bucket_name                  = "${var.deployment_id}-30-day-s3-ci-test-cors"
  force_destroy                = true
  lifecycle_policy_enforcement = "delete_everything_after_30_days"
  cors_rule = [
    {
      "allowed_headers" : [
        "*"
      ],
      "allowed_methods" : [
        "GET",
        "HEAD"
      ],
      "allowed_origins" : [
        "*"
      ],
      "expose_headers" : [],
      "max_age_seconds" : 3000
    }
  ]
}

module "this_with_no_lifecycles" {
  source                       = "../../"
  bucket_name                  = "${var.deployment_id}-30-day-s3-no-lifecycles"
  force_destroy                = true
  lifecycle_policy_enforcement = "no_lifecycles"
}

# There is a chicken and egg issue with cross account source buckets
# The destination bucket has to be created without a bucket policy (create_bucket_policy = false)
# Then the source bucket has to be created
# Then the destination bucket has to be created with the bucket policy added

#  module "this_default_source" {
#    source           = "../../"
#    bucket_name      = "${var.deployment_id}-s3-ci-test-source"
#    force_destroy    = true
#   replication_type = "source"
#   #This is required but there can't be created until the destination is created
#   destination_bucket_arn    = "arn:aws:s3:::123-s3-ci-test-destination"#"arn:aws:s3:::${var.deployment_id}-s3-ci-test-destination"
#   destination_storage_class = "STANDARD"
# }

# module "this_default_destination" {
#   source                    = "../../"
#   bucket_name               = "${var.deployment_id}-s3-ci-test-destination"
#   force_destroy             = true
#   replication_type          = "destination"
#   destination_storage_class = "STANDARD"
#   create_bucket_policy      = false
#   destination_account       = "776418794558"
#   bucket_policy_identifiers = [] #["${var.deployment_id}-s3-ci-test-destination"]
# }
