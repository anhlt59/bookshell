output "name" {
  value = aws_s3_bucket.this.id
}

output "arn" {
  value = aws_s3_bucket.this.arn
}

output "id" {
  value = aws_s3_bucket.this.id
}

output "role_arn" {
  value = ["${aws_iam_role.this_source_replication_role.*.name}"]
}

output "writer_policy_json" {
  value = data.aws_iam_policy_document.writer.json
}

output "domain" {
  value = aws_s3_bucket.this.bucket_domain_name
}

output "regional_domain_name" {
  value = aws_s3_bucket.this.bucket_regional_domain_name
}
