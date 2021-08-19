# Cluster instance autoscaling

1. adjust Cluster securitygroup
    * increase the _max capacity_ of the ASG (max no of instances) to e.g. 5

2. Create Capacity Provider
    * use cli
       * replace the ASG ARN in file
       * execute the following command

    ```bash
    aws ecs create-capacity-provider \
    --cli-input-json file://cp-ecs-ec2.json \
    --region eu-central-1
    ```

    * use AWS mgm console
        * open your ECS cluster overview in AWS management console
        * on the tab _Capacity Providers_ click _Create_
            * provide a name
            * select the ASG of your ECS cluster
            * **enable** the option _Managed scaling_ to enable automatic scale-out and -in
            * set _Target capacity_ to e.g. 70 (this means as soon as the instances within the ASG are 70% utilized, the managed scale-out kicks in, if enabled)
            * set _Managed termination protection_ to _disabled_

3. Set default Capacity Provider on ECS cluster level
    * open your ECS cluster overview in AWS management console
    * click on _Update Cluster_
    * select your Capacity Provider from step 2.





## create new ASG to be used by capacity provider

TAG Key "AmazonECSManaged" : Yes