data "aws_iam_policy_document" "source_destination_policy" {
  count = (var.replication_type == "destination" && var.create_bucket_policy == true) ? 1 : 0
  statement {
    sid    = "Set permissions on objects"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = var.bucket_policy_identifiers
    }
    actions = [
      "s3:ReplicateObject", "s3:ReplicateDelete"
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.this.id}/*"
    ]
  }

  statement {
    sid    = "Set permissions on bucket"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = var.bucket_policy_identifiers
    }
    actions = [
      "s3:List*", "s3:GetBucketVersioning", "s3:PutBucketVersioning"
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.this.id}"
    ]
  }

  statement {
    sid    = "Permission to override bucket owner"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = var.source_bucket_accounts
    }
    actions = [
      "s3:ObjectOwnerOverrideToBucketOwner",
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.this.id}/*"
    ]
  }
}
