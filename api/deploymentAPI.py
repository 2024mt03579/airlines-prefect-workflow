import requests

BASE_URL = "https://api.prefect.cloud/api"

# Prefect Cloud credentials and identifiers
PREFECT_API_KEY = "pnu_gjmyoKiUBsFU0LwyVSrELkLMwHJ85n1XHGcp"
ACCOUNT_ID = "f47937e7-20ac-4900-beba-f685f9892d9e"
WORKSPACE_ID = "d0f98ebd-01e3-482a-9c49-5761b5b20b34"
DEPLOYMENT_ID = "7267fef3-eeaa-4d77-8e56-8886ef9b1b5a"  # airline-dataset-workflow

PREFECT_API_URL = (
    f"{BASE_URL}/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/deployments/{DEPLOYMENT_ID}"
)


def get_deployment_details() -> dict:
    headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}
    response = requests.get(PREFECT_API_URL, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def list_deployments() -> list:
    """List all deployments in the configured workspace."""
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/deployments/filter"
    headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}
    response = requests.post(url, headers=headers, json={}, timeout=30)
    response.raise_for_status()
    return response.json()


def list_flows() -> list:
    """List all flows in the configured workspace."""
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/flows/filter"
    headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}
    response = requests.post(url, headers=headers, json={}, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        print("\n=== Deployments ===")
        for d in list_deployments():
            print(f"  ID: {d['id']}  |  Name: {d['name']}  |  Flow: {d.get('flow_id', 'N/A')}")

        print("\n=== Flows ===")
        for f in list_flows():
            print(f"  ID: {f['id']}  |  Name: {f['name']}")
    except requests.RequestException as exc:
        print(f"Error calling Prefect API: {exc}")
