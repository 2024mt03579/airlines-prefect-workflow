import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import requests

BASE_URL = "https://api.prefect.cloud/api"

try:
    api_dir = Path(__file__).resolve().parent
    if str(api_dir) not in sys.path:
        sys.path.insert(0, str(api_dir))
    import deploymentAPI as deployment_defaults

    DEFAULT_API_KEY = getattr(deployment_defaults, "PREFECT_API_KEY", None)
    DEFAULT_ACCOUNT_ID = getattr(
        deployment_defaults, "ACCOUNT_ID", "7f080b8b-43c7-4dcc-b351-396a3b3fe842"
    )
    DEFAULT_WORKSPACE_ID = getattr(
        deployment_defaults, "WORKSPACE_ID", "6cfccd6a-596e-4dcb-9dc1-4c35c015cc27"
    )
    DEFAULT_DEPLOYMENT_ID = getattr(deployment_defaults, "DEPLOYMENT_ID", None)
except Exception:
    DEFAULT_API_KEY = "pnu_gjmyoKiUBsFU0LwyVSrELkLMwHJ85n1XHGcp"
    DEFAULT_ACCOUNT_ID = "f47937e7-20ac-4900-beba-f685f9892d9e"
    DEFAULT_WORKSPACE_ID = "d0f98ebd-01e3-482a-9c49-5761b5b20b34"
    DEFAULT_DEPLOYMENT_ID = None

WORKSPACE_API_URL = (
    f"{BASE_URL}/accounts/{DEFAULT_ACCOUNT_ID}/workspaces/{DEFAULT_WORKSPACE_ID}"
)


def _build_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _get_json(url: str, headers: dict, timeout: int = 30) -> dict:
    response = requests.get(url, headers=headers, timeout=timeout)

    if response.status_code == 401:
        raise RuntimeError(
            "Not authenticated (401). Check PREFECT_API_KEY or --api-key and ensure it belongs to this account/workspace."
        )

    if response.status_code == 403:
        raise RuntimeError(
            "Forbidden (403). API key exists but does not have access to the requested account/workspace."
        )

    if not response.ok:
        raise RuntimeError(
            f"Request failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def get_flow_details(api_key: str, account_id: str, workspace_id: str, flow_id: str) -> dict:
    url = f"{BASE_URL}/accounts/{account_id}/workspaces/{workspace_id}/flows/{flow_id}"
    return _get_json(url, _build_headers(api_key))


def get_deployment_details(
    api_key: str, account_id: str, workspace_id: str, deployment_id: str
) -> dict:
    url = f"{BASE_URL}/accounts/{account_id}/workspaces/{workspace_id}/deployments/{deployment_id}"
    return _get_json(url, _build_headers(api_key))


def list_deployments(api_key: str, account_id: str, workspace_id: str) -> list:
    """Return all deployments in the workspace."""
    url = f"{BASE_URL}/accounts/{account_id}/workspaces/{workspace_id}/deployments/filter"
    response = requests.post(url, headers=_build_headers(api_key), json={}, timeout=30)
    if not response.ok:
        raise RuntimeError(f"list_deployments failed ({response.status_code}): {response.text}")
    return response.json()


def list_flows(api_key: str, account_id: str, workspace_id: str) -> list:
    """Return all flows in the workspace."""
    url = f"{BASE_URL}/accounts/{account_id}/workspaces/{workspace_id}/flows/filter"
    response = requests.post(url, headers=_build_headers(api_key), json={}, timeout=30)
    if not response.ok:
        raise RuntimeError(f"list_flows failed ({response.status_code}): {response.text}")
    return response.json()


def _read_value(cli_value: Optional[str], env_name: str, required: bool = True) -> Optional[str]:
    value = cli_value or os.getenv(env_name)
    if required and not value:
        raise RuntimeError(
            f"Missing value for {env_name}. Pass via CLI or set environment variable {env_name}."
        )
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Prefect Cloud flow/deployment details using API key authentication."
    )

    parser.add_argument("--api-key", help="Prefect API key (or set PREFECT_API_KEY)")
    parser.add_argument(
        "--account-id",
        default=DEFAULT_ACCOUNT_ID,
        help="Prefect Account ID (defaults to deploymentAPI.py/account env)",
    )
    parser.add_argument(
        "--workspace-id",
        default=DEFAULT_WORKSPACE_ID,
        help="Prefect Workspace ID (defaults to deploymentAPI.py/workspace env)",
    )

    parser.add_argument("--flow-id", help="Flow ID to fetch")
    parser.add_argument(
        "--deployment-id",
        default=DEFAULT_DEPLOYMENT_ID,
        help="Deployment ID to fetch (defaults to deploymentAPI.py)",
    )
    parser.add_argument(
        "--list-deployments",
        action="store_true",
        help="List all deployments in the workspace and exit",
    )
    parser.add_argument(
        "--list-flows",
        action="store_true",
        help="List all flows in the workspace and exit",
    )

    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()

        api_key = args.api_key or os.getenv("PREFECT_API_KEY") or DEFAULT_API_KEY
        if not api_key:
            raise RuntimeError(
                "Missing API key. Pass --api-key, set PREFECT_API_KEY, or define PREFECT_API_KEY in deploymentAPI.py."
            )

        account_id = args.account_id or os.getenv("PREFECT_ACCOUNT_ID") or DEFAULT_ACCOUNT_ID
        workspace_id = args.workspace_id or os.getenv("PREFECT_WORKSPACE_ID") or DEFAULT_WORKSPACE_ID

        # --- list modes (early exit) ---
        if args.list_deployments:
            deployments = list_deployments(api_key, account_id, workspace_id)
            print(f"\nFound {len(deployments)} deployment(s) in workspace:\n")
            for d in deployments:
                print(f"  Name : {d['name']}")
                print(f"  ID   : {d['id']}")
                print(f"  Flow : {d.get('flow_id', 'N/A')}")
                print(f"  Status: {d.get('status', 'N/A')}")
                print()
            return 0

        if args.list_flows:
            flows = list_flows(api_key, account_id, workspace_id)
            print(f"\nFound {len(flows)} flow(s) in workspace:\n")
            for f in flows:
                print(f"  Name : {f['name']}")
                print(f"  ID   : {f['id']}")
                print()
            return 0

        # --- fetch specific resource ---
        flow_id = _read_value(args.flow_id, "PREFECT_FLOW_ID", required=False)
        deployment_id = args.deployment_id or os.getenv("PREFECT_DEPLOYMENT_ID") or DEFAULT_DEPLOYMENT_ID

        if not flow_id and not deployment_id:
            raise RuntimeError(
                "Provide at least one of --flow-id, --deployment-id, --list-deployments, or --list-flows."
            )

        result = {}

        if flow_id:
            result["flow"] = get_flow_details(api_key, account_id, workspace_id, flow_id)

        if deployment_id:
            result["deployment"] = get_deployment_details(
                api_key, account_id, workspace_id, deployment_id
            )

        print(json.dumps(result, indent=2))
        return 0

    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
