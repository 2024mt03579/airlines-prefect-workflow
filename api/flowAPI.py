# URL - https://app.prefect.cloud/account/8ff8f613-92c4-44ce-b811-f9956023e78d/workspace/04d8fca9-df2e-40c8-ae4f-a3733114c475/dashboard

# URL - https://app.prefect.cloud/api/docs

import requests

# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_gjmyoKiUBsFU0LwyVSrELkLMwHJ85n1XHGcp"
ACCOUNT_ID = "f47937e7-20ac-4900-beba-f685f9892d9e"
WORKSPACE_ID = "d0f98ebd-01e3-482a-9c49-5761b5b20b34"
FLOW_ID = "adfaafb1-a9f7-4882-8041-bc1b8308f907"  # Your Flow ID for workflow.py

# Correct API URL to get flow details
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/flows/{FLOW_ID}"

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request using GET
response = requests.get(PREFECT_API_URL, headers=headers)

# Check the response status
if response.status_code == 200:
    flow_info = response.json()
    print(flow_info)
else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")
