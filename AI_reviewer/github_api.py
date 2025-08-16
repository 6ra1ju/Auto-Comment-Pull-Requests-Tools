import requests
from AI_reviewer.config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_open_pull_requests():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    response = requests.get(url, headers=headers)
    return response.json()

def get_pull_request_diff(pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    data = response.json()
    patches = [f['patch'] for f in data if 'patch' in f]
    diff = "\n".join(patches)
    return diff[:1500]  # giới hạn để tránh token quá dài

def post_comment_to_pr(pr_number, comment):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"
    data = {"body": f"🤖 **AI Reviewer**:\n\n{comment}"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        print(f"[ERROR] Failed to post comment: {response.status_code} - {response.text}")
    return response.status_code
