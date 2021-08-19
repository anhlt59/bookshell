# AWS ECS deep-dive course on Udemy

## Quickstart

- create IAM user
  log into AWS-mgm console and create new IAM user for this course, name it e.g. _eks-course_ and provide him policy permissions **AmazonECS-FullAccess**  and **AdministratorAccess**

- launch first container
  - using wizard in AWS-mgm console, starting webserver nginx container on Fargate

## Course Hands-On lectures

- [Docker basics](./docker-basics/Readme.md)
- [ECS setup](./ecs-setup/Readme.md)
- [Loadbalancing & autoscaling](./Loadbalancing-and-Autoscaling/Readme.md)
- [Environment variables](./Env-variables/Readme.md)
- [ECR](./ECR/Readme.md)
- CI/CD
  - [CodeCommit](./CICD/CodeCommit/Readme.md)
  - [CodeBuild](./CICD/CodeBuild/Readme.md)
  - [CodePipeline](./CICD/CodePipeline/Readme.md)
  - [Blue/Green deployment w/ CodeDeploy](./CICD/Blue-Green-with-CodeDeploy/Readme.md)
- [EFS - persistent storage](./EFS-Persistent-storage/Readme.md)
- [Microservices - XRay/AppMesh/CloudMap](./Microservices-XRay-AppMesh/Readme.md)