locals {
  main = {
    "lifecycle_rules" : {
      "default" : {
        "transition" : [],
        "noncurrent_version_transition" : [{
          "days" : 30,
          "storage_class" : "STANDARD_IA",
          },
          {
            "days" : 60,
            "storage_class" : "GLACIER"
          }
        ],
        "expiration" : [],
        "noncurrent_version_expiration" : [{
          "days" : 90
          }
        ]
      },
      "delete_everything_after_30_days" : {
        # Expiration does not inlclude noncurrent object versions
        "noncurrent_version_transition" : [],
        "expiration" : [{
          "days" : 30,
          }
        ],
        "noncurrent_version_expiration" : [{
          "days" : 30
          }
        ],
        "transition" : []
      },
      "delete_everything_after_n_days" : {
        # Expiration does not inlclude noncurrent object versions
        "noncurrent_version_transition" : [],
        "expiration" : [{
          "days" : var.retention_days,
          }
        ],
        "noncurrent_version_expiration" : [{
          "days" : var.retention_days
          }
        ],
        "transition" : []
      },
      "custom" : {
        # Expiration does not inlclude noncurrent object versions
        "noncurrent_version_transition" : [{
          "days" : var.custom_domain_main_lifecycle["noncurrent_ia_days"],
          "storage_class" : "STANDARD_IA",
          },
          {
            "days" : var.custom_domain_main_lifecycle["noncurrent_glacier_days"],
            "storage_class" : "GLACIER"
        }],
        "noncurrent_version_expiration" : [{
          "days" : var.custom_domain_main_lifecycle["noncurrent_retention_days"],
        }],
        "transition" : [{
          "days" : var.custom_domain_main_lifecycle["regular_ia_days"],
          "storage_class" : "STANDARD_IA",
          },
          {
            "days" : var.custom_domain_main_lifecycle["regular_glacier_days"],
            "storage_class" : "GLACIER"
        }],
        "expiration" : [{
          "days" : var.custom_domain_main_lifecycle["regular_retention_days"],
          }
        ]
      },
      "no_lifecycles" : {
        "noncurrent_version_transition" : [],
        "expiration" : [],
        "noncurrent_version_expiration" : [],
        "transition" : []
      },
    }
  }
  access_logs = {
    "lifecycle_rules" : {
      "default" : {
        "transition" : [{
          "days" : 30,
          "storage_class" : "STANDARD_IA",
          },
          {
            "days" : 60,
            "storage_class" : "GLACIER"
          }
        ],
        "noncurrent_version_transition" : [],
        "expiration" : [{
          "days" : 365
          }
        ],
        "noncurrent_version_expiration" : []
      },
      "delete_everything_after_30_days" : {
        "transition" : [],
        "noncurrent_version_transition" : [],
        "expiration" : [{
          "days" : 30
          }
        ],
        "noncurrent_version_expiration" : [],
      },
      "delete_everything_after_n_days" : {
        "transition" : [],
        "noncurrent_version_transition" : [],
        "expiration" : [{
          "days" : var.retention_days
          }
        ],
        "noncurrent_version_expiration" : [],
      },
      "custom" : {
        "transition" : [{
          "days" : var.custom_domain_access_logs_lifecycle["regular_ia_days"],
          "storage_class" : "STANDARD_IA",
          },
          {
            "days" : var.custom_domain_access_logs_lifecycle["regular_glacier_days"],
            "storage_class" : "GLACIER"
        }],
        "noncurrent_version_transition" : [],
        "noncurrent_version_expiration" : [],
        "expiration" : [{
          "days" : var.custom_domain_access_logs_lifecycle["regular_retention_days"],
          }
        ]
      },
      "no_lifecycles" : {
        "noncurrent_version_transition" : [],
        "expiration" : [],
        "noncurrent_version_expiration" : [],
        "transition" : []
      },
    }
  }
}

resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  acl    = var.acl

  force_destroy = var.force_destroy

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  logging {
    target_bucket = aws_s3_bucket.access_logs.id
    target_prefix = "log/"
  }

  dynamic "cors_rule" {
    for_each = var.cors_rule
    content {
      allowed_headers = cors_rule.value.allowed_headers
      allowed_methods = cors_rule.value.allowed_methods
      allowed_origins = cors_rule.value.allowed_origins
      expose_headers  = cors_rule.value.expose_headers
      max_age_seconds = cors_rule.value.max_age_seconds
    }
  }

  # Delete old versions after some time
  dynamic "lifecycle_rule" {
    for_each = (length(local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_transition"]) == 0 && length(local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_expiration"]) == 0 && length(local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["transition"]) == 0 && length(local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["expiration"]) == 0) ? [] : [1]

    content {
      enabled = true
      dynamic "noncurrent_version_transition" {
        for_each = local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_transition"]
        content {
          days          = noncurrent_version_transition.value["days"]
          storage_class = noncurrent_version_transition.value["storage_class"]
        }
      }

      dynamic "noncurrent_version_expiration" {
        for_each = local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_expiration"]
        content {
          days = noncurrent_version_expiration.value["days"]
        }
      }

      dynamic "transition" {
        for_each = local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["transition"]
        content {
          days          = transition.value["days"]
          storage_class = transition.value["storage_class"]
        }
      }

      dynamic "expiration" {
        for_each = local.main["lifecycle_rules"][var.lifecycle_policy_enforcement]["expiration"]
        content {
          days = expiration.value["days"]
        }
      }
    }
  }

  dynamic "replication_configuration" {
    for_each = var.replication_type == "source" ? [1] : []
    content {
      role = aws_iam_role.this_source_replication_role.0.arn

      rules {
        id     = "replication"
        prefix = ""
        status = "Enabled"

        destination {
          bucket        = var.destination_bucket_arn
          storage_class = var.destination_storage_class
        }
      }
    }
  }
}

resource "aws_s3_bucket" "access_logs" {
  bucket = "${var.bucket_name}-access-logs"
  acl    = "log-delivery-write"

  force_destroy = var.force_destroy

  versioning {
    enabled = false
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  dynamic "lifecycle_rule" {
    for_each = (length(local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_transition"]) == 0 && length(local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_expiration"]) == 0 && length(local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["transition"]) == 0 && length(local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["expiration"]) == 0) ? [] : [1]

    content {
      enabled = true
      dynamic "noncurrent_version_transition" {
        for_each = local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_transition"]
        content {
          days          = noncurrent_version_transition.value["days"]
          storage_class = noncurrent_version_transition.value["storage_class"]
        }
      }

      dynamic "noncurrent_version_expiration" {
        for_each = local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["noncurrent_version_expiration"]
        content {
          days = noncurrent_version_expiration.value["days"]
        }
      }

      dynamic "transition" {
        for_each = local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["transition"]
        content {
          days          = transition.value["days"]
          storage_class = transition.value["storage_class"]
        }
      }

      dynamic "expiration" {
        for_each = local.access_logs["lifecycle_rules"][var.lifecycle_policy_enforcement]["expiration"]
        content {
          days = expiration.value["days"]
        }
      }
    }
  }
}

resource "aws_iam_role" "this_source_replication_role" {
  count = var.replication_type == "source" ? 1 : 0
  name  = "source-replication-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "this_source_replication_policy" {
  count  = var.replication_type == "source" ? 1 : 0
  name   = "source-replication-policy"
  policy = data.aws_iam_policy_document.source_replication_policy.0.json
}

resource "aws_iam_role_policy_attachment" "this_source_replication_attachment" {
  count      = var.replication_type == "source" ? 1 : 0
  role       = aws_iam_role.this_source_replication_role.0.name
  policy_arn = aws_iam_policy.this_source_replication_policy.0.arn
}

resource "aws_s3_bucket_policy" "destination" {
  count  = (var.replication_type == "destination" && var.create_bucket_policy == true) ? 1 : 0
  bucket = aws_s3_bucket.this.id
  policy = data.aws_iam_policy_document.source_destination_policy.0.json
}
