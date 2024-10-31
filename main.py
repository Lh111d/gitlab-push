import logging

import requests
from flask import Flask, request, jsonify
from push_lark import push

import config

# 配置日志
log_file = "./logging.log"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app = Flask(__name__)


def get_commit(project_id):
    gitlab_access_token = config.gitlab_access_token
    headers = {
        "PRIVATE-TOKEN": gitlab_access_token,
        "Content-Type": "application/json"
    }
    base_api = config.base_api
    # 获取最新的 commit 信息
    url = f"{base_api}/projects/{project_id}/repository/commits?per_page=1"
    response = requests.get(url, headers=headers)

    # 打印最新的 commit 信息
    if response.status_code == 200:
        commits = response.json()
        if commits:
            latest_commit = commits[0]  # 取第一个即为最新的 commit
            logging.info(f"Latest commit {latest_commit['id']}")
            print(f"Latest Commit ID: {latest_commit['id']}")
            logging.info(f"Latest Commit Message: {latest_commit['message']}")

            print(f"Date: {latest_commit['created_at']}")

            return latest_commit['message'], latest_commit['created_at']
        else:
            print("No commits found.")
            logging.info(f"No commits found.")
            return "No commits found."
    else:
        print(f"Error: {response.status_code} - {response.text}")
        logging.info(f"Error: {response.status_code} - {response.text}")
        return ""


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)
    object_kind = data['object_kind']
    project_id = data['project_id']
    project_url = data['project_url']
    project_name = data['project_name']
    message, create_time = get_commit(project_id)
    if push(object_kind, project_id, project_name, project_url, message, create_time):
        logging.info(f"Push Commit: {message}")
        return jsonify({"status": "success", "push": "推送成功"}), 200
    else:
        logging.info(f"Push Commit: {message}")
        return jsonify({"status": "failure", "push": "推送失败"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6351)
