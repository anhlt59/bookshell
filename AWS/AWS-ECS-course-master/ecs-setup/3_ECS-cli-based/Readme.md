# Create ECS cluster via ecs-cli

## grab required properties

### on Linux

```bash
export CORE_STACK_NAME="ecs-core-infrastructure"
export vpc=$(aws cloudformation describe-stacks --stack-name $CORE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`VpcId`].OutputValue' --output text)
export subnet_1=$(aws cloudformation describe-stacks --stack-name $CORE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`PublicSubnetOne`].OutputValue' --output text)
export subnet_2=$(aws cloudformation describe-stacks --stack-name $CORE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`PublicSubnetTwo`].OutputValue' --output text)

echo "vpc: $vpc"
echo "subnet1: $subnet_1"
echo "subnet2: $subnet_2"

```

### via AWS mgm console

* open AWS mgm console
* go to service "_CloudFormation_"
* check tab "_Outputs_" of stack "_ecs-core-infrastructure_" and get the IDs for VPC and both subnets

## create ecs cluster with launch-type FARGATE

```bash

ecs-cli up \
--subnets $subnet_1,$subnet_2 \
--vpc $vpc \
--launch-type FARGATE \
--cluster ecs-fargate
```

## do the same, but with additional properties to create an ecs cluster with launch-type EC2

```bash

ecs-cli up --capability-iam \
--subnets $subnet_1,$subnet_2 \
--vpc $vpc \
--launch-type EC2 \
--keypair ecs-course \
--size 1 \
--instance-type t2.small \
--cluster ecs-ec2
```
