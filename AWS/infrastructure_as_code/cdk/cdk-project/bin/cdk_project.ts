#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CdkCoreStack } from '../lib/cdk-core-stack';
import { CdkEdgeStack } from '../lib/cdk-edge-stack';

interface Environments {
  account: string;
  region: string;
}
const coreEnv: Environments = { account: '315941280866', region: 'eu-central-1' };
// const edgeEnv: Environments = { account: '315941280866', region: 'us-east-1' };

const app = new cdk.App();
new CdkCoreStack(app, 'CdkCoreStack', { env: coreEnv });
// new CdkEdgeStack(app, 'CdkEdgeStack', { env: edgeEnv });
