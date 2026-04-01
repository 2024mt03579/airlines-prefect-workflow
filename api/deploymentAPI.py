import requests

BASE_URL = "https://api.prefect.cloud/api"

# Prefect Cloud credentials and identifiers
PREFECT_API_KEY = "pnu_utO6Fjs1jiqtUwqIKG6rmjp8gonrbo392G0K"
ACCOUNT_ID = "7f080b8b-43c7-4dcc-b351-396a3b3fe842"
WORKSPACE_ID = "6cfccd6a-596e-4dcb-9dc1-4c35c015cc27"
DEPLOYMENT_ID = "c0dbd294-fb2c-413c-9a74-45d80158b731"  # airline-dataset-workflow

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
