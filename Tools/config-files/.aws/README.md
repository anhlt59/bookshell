
### Configure profile
```sh
$ aws configure [--profile profile-name]
AWS Access Key ID [****]:
AWS Secret Access Key [****]:
Default region name [us-west-1]: us-west-2
Default output format [None]: json
```
### To use profile
```sh
$ aws s3 ls --profile anhlt
2022-04-29 05:13:45 aws-cloudtrail-logs-251623506909-f823bf53
2022-05-14 00:42:09 cdk-cbi303zid-assets-251623506909-us-east-1
2021-11-03 17:55:19 cdk-hnb659fds-assets-251623506909-us-east-1
2022-05-15 02:21:07 cdk-hnb659fds-assets-251623506909-us-east-2
...
```
