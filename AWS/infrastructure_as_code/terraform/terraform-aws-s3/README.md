# S3 bucket

This deploys an S3 bucket:

- private ACL
- encrypted
- versioned (with lifecycle policy on non-current version)
- access logging (with lifecycle policy on logs)

This configuration is appropriate for Cerebral application use. A writer policy is provided in an output that is
appropriate to assign to Cerebral workloads requiring an S3 bucket.

## Replication

There is a chicken and egg issue with cross account source buckets. The destination bucket has to be created without a
bucket policy (create_bucket_policy = false). Then the source bucket has to be created. Then the default destination
bucket has to be created with the bucket policy added.

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.this_source_replication_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.this_source_replication_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.this_source_replication_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_s3_bucket.access_logs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_policy.destination](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy) | resource |
| [aws_iam_policy_document.source_destination_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.source_replication_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.writer](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_acl"></a> [acl](#input\_acl) | What is the canned ACL of this bucket. Valid values are private, public-read, public-read-write, aws-exec-read, authenticated-read, and log-delivery-write. Defaults to private. Conflicts with grant. | `string` | `"private"` | no |
| <a name="input_bucket_name"></a> [bucket\_name](#input\_bucket\_name) | What to name the bucket | `any` | n/a | yes |
| <a name="input_bucket_policy_identifiers"></a> [bucket\_policy\_identifiers](#input\_bucket\_policy\_identifiers) | List of bucket policy identifiers to allow | `list(string)` | `[]` | no |
| <a name="input_create_bucket_policy"></a> [create\_bucket\_policy](#input\_create\_bucket\_policy) | Should breate bucket policy | `bool` | `false` | no |
| <a name="input_custom_domain_access_logs_lifecycle"></a> [custom\_domain\_access\_logs\_lifecycle](#input\_custom\_domain\_access\_logs\_lifecycle) | Custom domain lifecycle for the main bucket | `map(number)` | <pre>{<br>  "regular_glacier_days": 60,<br>  "regular_ia_days": 30,<br>  "regular_retention_days": 90<br>}</pre> | no |
| <a name="input_custom_domain_main_lifecycle"></a> [custom\_domain\_main\_lifecycle](#input\_custom\_domain\_main\_lifecycle) | Custom domain lifecycle for the main bucket | `map(number)` | <pre>{<br>  "noncurrent_glacier_days": 60,<br>  "noncurrent_ia_days": 30,<br>  "noncurrent_retention_days": 90,<br>  "regular_glacier_days": 60,<br>  "regular_ia_days": 30,<br>  "regular_retention_days": 90<br>}</pre> | no |
| <a name="input_destination_account"></a> [destination\_account](#input\_destination\_account) | The source account | `string` | `""` | no |
| <a name="input_destination_bucket_arn"></a> [destination\_bucket\_arn](#input\_destination\_bucket\_arn) | The destination bucket arn | `string` | `""` | no |
| <a name="input_destination_storage_class"></a> [destination\_storage\_class](#input\_destination\_storage\_class) | The destination storage class | `string` | `""` | no |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | Should the S3 bucket be destroyed even when it has objects? | `bool` | `false` | no |
| <a name="input_lifecycle_policy_enforcement"></a> [lifecycle\_policy\_enforcement](#input\_lifecycle\_policy\_enforcement) | Can be either default, delete\_everything\_after\_30\_days, or delete\_everything\_after\_n\_days (in which case 'retention\_days' should be set) | `string` | `"default"` | no |
| <a name="input_replication_type"></a> [replication\_type](#input\_replication\_type) | The type of replication. This specifices whether this is a source or destination bucket. Set source if the bucket is a source and destination if it is a destination | `string` | `"default"` | no |
| <a name="input_retention_days"></a> [retention\_days](#input\_retention\_days) | How many days to retain objects? Ignored unless lifecycle\_policy\_enforcement is 'delete\_everything\_after\_n\_days' | `number` | `30` | no |
| <a name="input_source_bucket_accounts"></a> [source\_bucket\_accounts](#input\_source\_bucket\_accounts) | Source bucket accounts | `list(string)` | `[]` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | n/a |
| <a name="output_domain"></a> [domain](#output\_domain) | n/a |
| <a name="output_id"></a> [id](#output\_id) | n/a |
| <a name="output_name"></a> [name](#output\_name) | n/a |
| <a name="output_regional_domain_name"></a> [regional\_domain\_name](#output\_regional\_domain\_name) | n/a |
| <a name="output_role_arn"></a> [role\_arn](#output\_role\_arn) | n/a |
| <a name="output_writer_policy_json"></a> [writer\_policy\_json](#output\_writer\_policy\_json) | n/a |