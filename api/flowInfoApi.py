import json
import requests

PREFECT_API_KEY = "pnu_gjmyoKiUBsFU0LwyVSrELkLMwHJ85n1XHGcp"
ACCOUNT_ID = "f47937e7-20ac-4900-beba-f685f9892d9e"
WORKSPACE_ID = "d0f98ebd-01e3-482a-9c49-5761b5b20b34"
FLOW_ID = "adfaafb1-a9f7-4882-8041-bc1b8308f907"

BASE_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}"

headers = {
    "Authorization": f"Bearer {PREFECT_API_KEY}",
    "Content-Type": "application/json"
}

# -------------------------------
# 1. Get Flow Info
# -------------------------------
flow_url = f"{BASE_URL}/flows/{FLOW_ID}"
flow_response = requests.get(flow_url, headers=headers)

if flow_response.status_code == 200:
    flow_info = flow_response.json()
else:
    print("Error fetching flow info:", flow_response.text)
    flow_info = {}

# -------------------------------
# 2. Get Flow Runs
# -------------------------------
runs_url = f"{BASE_URL}/flow_runs/filter"

payload = {
    "flows": {
        "id": {
            "any_": [FLOW_ID]
        }
    },
    "sort": "START_TIME_DESC",
    "limit": 10
}

runs_response = requests.post(runs_url, headers=headers, json=payload)

if runs_response.status_code == 200:
    flow_runs = runs_response.json()
else:
    print("Error fetching flow runs:", runs_response.text)
    flow_runs = []

# -------------------------------
# 3. Combine & Beautify Output
# -------------------------------
output = {
    "flow_info": flow_info,
    "recent_runs": flow_runs
}

print(json.dumps(output, indent=4))