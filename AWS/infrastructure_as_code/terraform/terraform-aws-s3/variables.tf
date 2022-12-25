terraform {
  # Optional attributes and the defaults function are
  # both experimental, so we must opt in to the experiment.
  experiments = [module_variable_optional_attrs]
}

variable "bucket_name" {
  description = "What to name the bucket"
}

variable "force_destroy" {
  description = "Should the S3 bucket be destroyed even when it has objects?"
  default     = false
}

variable "acl" {
  description = "What is the canned ACL of this bucket. Valid values are private, public-read, public-read-write, aws-exec-read, authenticated-read, and log-delivery-write. Defaults to private. Conflicts with grant."
  type        = string
  default     = "private"
}

variable "lifecycle_policy_enforcement" {
  description = "Can be either default, delete_everything_after_30_days, or delete_everything_after_n_days (in which case 'retention_days' should be set)"
  type        = string
  default     = "default"
}

variable "retention_days" {
  description = "How many days to retain objects? Ignored unless lifecycle_policy_enforcement is 'delete_everything_after_n_days'"
  type        = number
  default     = 30
}

variable "replication_type" {
  description = "The type of replication. This specifices whether this is a source or destination bucket. Set source if the bucket is a source and destination if it is a destination"
  type        = string
  default     = "default"
}

variable "destination_bucket_arn" {
  description = "The destination bucket arn"
  type        = string
  default     = ""
}

variable "destination_account" {
  description = "The source account"
  type        = string
  default     = ""
  validation {
    condition     = var.destination_account == "776418794558" || var.destination_account == ""
    error_message = "That is not the security account."
  }
}

variable "destination_storage_class" {
  description = "The destination storage class"
  type        = string
  default     = ""
}

variable "create_bucket_policy" {
  description = "Should breate bucket policy"
  type        = bool
  default     = false
}

variable "bucket_policy_identifiers" {
  description = "List of bucket policy identifiers to allow"
  type        = list(string)
  default     = []
}

variable "source_bucket_accounts" {
  description = "Source bucket accounts"
  type        = list(string)
  default     = []
}


variable "custom_domain_main_lifecycle" {
  description = "Custom domain lifecycle for the main bucket"
  type        = map(number)
  # Contains all keys
  # 0 will fail
  default = {
    noncurrent_ia_days        = 30
    noncurrent_glacier_days   = 60
    noncurrent_retention_days = 90
    regular_ia_days           = 30
    regular_glacier_days      = 60
    regular_retention_days    = 90
  }
}

variable "custom_domain_access_logs_lifecycle" {
  description = "Custom domain lifecycle for the main bucket"
  type        = map(number)
  # Contains all keys
  # 0 will fail
  default = {
    regular_ia_days        = 30
    regular_glacier_days   = 60
    regular_retention_days = 90
  }
}

variable "cors_rule" {
  description = "Custom domain lifecycle for the main bucket"
  default     = []
  type = list(object({
    allowed_headers = list(string)
    allowed_methods = list(string)
    allowed_origins = list(string)
    expose_headers  = list(string)
    # Default is 0
    max_age_seconds = number
  }))
}

variable "enable_metrics" {
  description = "Enable S3 bucket request metrics? https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudwatch-monitoring.html"
  default     = false
}
