data "aws_iam_policy_document" "source_replication_policy" {
  count = var.replication_type == "source" ? 1 : 0
  statement {
    effect = "Allow"
    actions = [
      "s3:GetReplicationConfiguration",
      "s3:ListBucket"
    ]

    resources = [
      "${aws_s3_bucket.this.arn}"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObjectVersionForReplication",
      "s3:GetObjectVersionAcl",
      "s3:GetObjectVersionTagging"
    ]

    resources = [
      "${aws_s3_bucket.this.arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags"
    ]

    resources = [
      "${var.destination_bucket_arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ObjectOwnerOverrideToBucketOwner"
    ]

    resources = [
      "${var.destination_bucket_arn}/*"
    ]
  }
}
