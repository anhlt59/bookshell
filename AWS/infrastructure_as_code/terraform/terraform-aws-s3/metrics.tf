resource "aws_s3_bucket_metric" "this" {
  count  = var.enable_metrics ? 1 : 0
  bucket = aws_s3_bucket.this.bucket
  name   = "${var.bucket_name}-bucket-metrics"
}
