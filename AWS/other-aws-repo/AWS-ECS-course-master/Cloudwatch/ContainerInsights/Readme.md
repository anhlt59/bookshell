# Container Insights  

## Enable Container insights on cluster level
Execute the following command to enable Container Insights on the cluster. This command will enable **Service and Cluster level** insights on your ECS cluster

```bash

aws ecs update-cluster-settings \
--cluster ecs-ec2  \
--settings name=containerInsights,value=enabled \
--region eu-central-1

```

## Container logs into Cloudwatch

1. Go to Cloudwatch Logs and in the _Action_ menu choose **Create log group** and provide a unique structure, e.g. /ecs/tasks/simplehttp
2. Go to the task definition and enable **Log configuration** in the _Storage and Logging_ section.
3. Select **awslogs** as Log driver
4. Provide the Log group name from step 1. as Value for Key _awslogs-group_


## Enable Instance Level Insights  
The following command will install **Instance level** insights on the ECS cluster.

```bash

aws cloudformation create-stack \
--stack-name CWAgentECS-ecs-ec2-eu-central-1 \
--template-body "$(curl -Ls https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/ecs-task-definition-templates/deployment-mode/daemon-service/cwagent-ecs-instance-metric/cloudformation-quickstart/cwagent-ecs-instance-metric-cfn.json)" \
--parameters ParameterKey=ClusterName,ParameterValue=ecs-ec2 \
    ParameterKey=TaskRoleArn,ParameterValue=arn:aws:iam::258889785048:role/ecsTaskExecutionRole \
    ParameterKey=ExecutionRoleArn,ParameterValue=arn:aws:iam::258889785048:role/ecsTaskExecutionRole \
--region eu-central-1
```

## Cleanup

### disable container insights on cluster level

```bash
aws ecs update-cluster-settings \
--cluster ecs-ec2  \
--settings name=containerInsights,value=disabled \
--region eu-central-1
```

### disable container insights on instance level

```bash
aws cloudformation delete-stack \
--stack-name CWAgentECS-ecs-ec2-eu-central-1 \
--region eu-central-1
```

### disable logging on container level

* update the task definition by setting "_logdriver_" to "_none_" in the container details => section _Storage and Logging_
* redeploy the simplehttp-service with the new task definition revision number