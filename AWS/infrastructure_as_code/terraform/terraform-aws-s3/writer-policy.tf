data "aws_iam_policy_document" "writer" {

  statement {
    actions = [
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.this.arn,
    ]
  }

  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject"
    ]

    resources = [
      "${aws_s3_bucket.this.arn}/*"
    ]
  }
}
