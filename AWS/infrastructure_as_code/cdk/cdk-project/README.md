# Welcome to your CDK TypeScript project
This is a blank project for CDK development with TypeScript.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Setup
```sh
$ npm install -g aws-cdk
$ cdk init app --language typescript
$ npm install
```

## Useful commands
NPM Command                           | Description
--------------------------------------|---------------------------------------------------------------------------------
`npm run build`                       | compile typescript to js
`npm run watch`                       | watch for changes and compile
`npm run test`                        | perform the jest unit tests


CDK Command                               | Description
--------------------------------------|---------------------------------------------------------------------------------
`cdk docs`                            | Access the online documentation
`cdk init`                            | Start a new CDK project (app or library)
`cdk list`                            | List stacks in an application
`cdk synth`                           | Synthesize a CDK app to CloudFormation template(s)
`cdk diff`                            | Diff stacks against current state
`cdk deploy`                          | Deploy a stack into an AWS account
`cdk import`                          | Import existing AWS resources into a CDK stack
`cdk watch`                           | Watches a CDK app for deployable and hotswappable changes
`cdk destroy`                         | Deletes a stack from an AWS account
`cdk bootstrap`                       | Deploy a toolkit stack to support deploying large stacks & artifacts (contain s3 bucket (stores file assets), ecr repo (stores images), iam role (Deployment Action Role, CloudFormation Execution Role))
`cdk doctor`                          | Inspect the environment and produce information useful for troubleshooting
`cdk acknowledge`                     | Acknowledge (and hide) a notice by issue number
`cdk notices`                         | List all relevant notices for the application
