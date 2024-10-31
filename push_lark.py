import requests
import json
import config


def push(object_kind, project_id, project_name, project_url, message, create_time):
    # Webhook URL
    webhook_url = config.webhook

    headers = {
        'Content-Type': 'application/json',
    }
    # 构建消息数据
    params = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"🤖 {object_kind} triggered",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": f"Project id: {project_id}\nProject name: {project_name}\n"
                            },
                            {
                                "tag": "text",
                                "text": f"Commit message: {message} Commit time: {create_time}\nProject URL: "
                            },
                            {
                                "tag": "a",
                                "text": "link",
                                "href": project_url
                            }
                        ]
                    ]
                }
            }
        }
    }

    # 发送 POST 请求
    response = requests.post(webhook_url, json=params, headers=headers)
    print(response)
    # 检查响应
    if response.status_code == 200:
        print("消息发送成功")
        return True
    else:
        print("发送失败:", response.status_code, response.text)
        return False