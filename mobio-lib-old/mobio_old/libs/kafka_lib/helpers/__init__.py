import os
from datetime import datetime
import requests


def consumer_warning_slack(pod_name, group_id, pretext="Consumer restart"):
    url = os.environ.get("SLACK_URI_RESTART_POD")
    if url:
        try:
            data_json = {
                "attachments": [
                    {
                        "color": "#dc3907",
                        "pretext": pretext,
                        "title": "Pod name: {}".format(pod_name),
                        "author_name": "Group Name: {}".format(group_id),
                        "text": "Time: {}".format(datetime.utcnow()),
                        "fields": [
                            {
                                "title": "Date",
                                "value": str(datetime.utcnow()),
                                "short": True,
                            },
                            {"title": "Host", "value": pod_name, "short": True},
                            {"title": "VM", "value": os.getenv('VM_TYPE', None), "short": True},
                        ],
                    }
                ]
            }
            response = requests.post(url, json=data_json)
            print(response.text)

        except Exception as ex:
            print("Error: ", ex)
    else:
        print("env SLACK_URI_RESTART_POD not exists")
