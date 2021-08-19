# EFS integration

https://aws.amazon.com/blogs/containers/developers-guide-to-using-amazon-efs-with-amazon-ecs-and-aws-fargate-part-1/

## Create EFS filesystem

Use AWS mgm console to create
* SecurityGroup for EFS
* EFS file system
* EFS mount targets
* EFS accesspoint

## Extend taskExecutionRole

To be able to mount EFS targets, the taskExecutionRole needs the proper IAM permissions. Add the following JSON policy as _inline policy_ to the _taskExecutionRole_ , replacing the placeholders in:  
* EFS ARN
  * REGION
  * ACCOUNT_ID
  * fs-xxxxxx
* EFS Accesspoint ARN
  * REGION
  * ACCOUNT_ID
  * fsap-xxxxxxxxxxxxxx


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticfilesystem:ClientMount",
                "elasticfilesystem:ClientWrite"
            ],
            "Resource": "arn:aws:elasticfilesystem:REGION:ACCOUNT_ID:file-system/fs-xxxxxx",
            "Condition": {
                "StringEquals": {
                    "elasticfilesystem:AccessPointArn": "arn:aws:elasticfilesystem:REGION:ACCOUNT_ID:access-point/fsap-xxxxxxxxxxxxx"
                }
            }
        }
    ]
}
```

