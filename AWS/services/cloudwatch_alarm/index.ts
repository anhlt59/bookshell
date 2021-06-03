import * as AWS from 'aws-sdk';
import ejs = require('ejs');

const REGION = process.env.REGION || 'us-east-1';
const STAGE = process.env.STAGE || 'development';
const SNS_TOPIC_ARN = process.env.SNS_TOPIC_ARN || '';

const sns = new AWS.SNS({region: REGION});
const cloudwatch = new AWS.CloudWatch({region: REGION});

const SUBJECT = 'ALARM: <%= AlarmName; %>';
const BODY = `
You are receiving this email because your Amazon CloudWatch Alarm “<%= AlarmName; %>” has entered the ALARM state, at “<%= StateUpdatedTimestamp; %>“. 

Alarm Details:
- Name: <%= AlarmName; %>
- Description: This alarm gets triggered when the Alarm Status changed to ALARM.
- State Change: OK - > ALARM
- Reason for State Change: <%= StateReason; %>
- Timestamp: <%= StateUpdatedTimestamp; %>

View this alarm in the AWS console:
https://us-east-1.console.aws.amazon.com/cloudwatch/deeplink.js?region=us-east-1#alarmsV2:alarm/<%= AlarmName; %>`


async function getAlarms(prefix: string) {
  const {MetricAlarms} = await cloudwatch.describeAlarms({
    AlarmNamePrefix: prefix,
    AlarmTypes: ['MetricAlarm']
  }).promise();
  return MetricAlarms || [];
}


exports.lambdaHandler = async (event: any) => {
  const alarms = await getAlarms(`materially-${STAGE}`);

  for (const alarm of alarms) {
    if (alarm.AlarmName) {
      // check alarm status
      if (alarm.StateValue === "ALARM") {
        // send message to SNS notification topic if alarmStatus = 'ALARM'
        await sns.publish({
          Subject: SUBJECT,
          Message: ejs.render(BODY, alarm),
          TopicArn: SNS_TOPIC_ARN,
        }).promise();
        console.log(`sns publish ${subject}`);
      }
    }
  }
}