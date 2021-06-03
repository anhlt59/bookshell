import os
import sys

import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/<your>/<slack>/<webhook>"
SLACK_CHANNEL = "#your-slack-channel"
ALERT_STATE = sys.argv[1]

alert_map = {
    "emoji": {"up": ":white_check_mark:", "down": ":fire:"},
    "text": {"up": "RESOLVED", "down": "FIRING"},
    "message": {"up": "Everything is good!", "down": "Stuff is burning!"},
    "color": {"up": "#32a852", "down": "#ad1721"},
}


def alert_to_slack(status, log_url, metric_url):
    data = {
        "text": "AlertManager",
        "username": "Notifications",
        "channel": SLACK_CHANNEL,
        "attachments": [
            {
                "text": "{emoji} [*{state}*] Status Checker\n {message}".format(
                    emoji=alert_map["emoji"][status],
                    state=alert_map["text"][status],
                    message=alert_map["message"][status],
                ),
                "color": alert_map["color"][status],
                "attachment_type": "default",
                "actions": [
                    {"name": "Logs", "text": "Logs", "type": "button", "style": "primary", "url": log_url},
                    {"name": "Metrics", "text": "Metrics", "type": "button", "style": "primary", "url": metric_url},
                ],
            }
        ],
    }
    r = requests.post(SLACK_WEBHOOK_URL, json=data)
    return r.status_code


alert_to_slack(ALERT_STATE, "https://grafana-logs.dashboard.local", "https://grafana-metrics.dashboard.local")
