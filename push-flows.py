import requests
import json

# Floodlight REST API base URL
FLOODLIGHT_API_BASE = "http://localhost:8080"

# Function to push a static flow
def push_static_flow(flow_name, switch_id, in_port, out_port, priority=1000):
    """
    Push a static flow to the Floodlight controller.
    :param flow_name: Name of the flow
    :param switch_id: Switch DPID
    :param in_port: Input port number
    :param out_port: Output port number
    :param priority: Priority of the flow
    """
    flow = {
        "switch": switch_id,
        "name": flow_name,
        "priority": str(priority),
        "eth_type": "0x0800",  # IPv4
        "in_port": str(in_port),
        "active": "true",
        "actions": f"output={out_port}"
    }

    url = f"{FLOODLIGHT_API_BASE}/wm/staticflowpusher/json"
    response = requests.post(url, data=json.dumps(flow), headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        print(f"Flow '{flow_name}' successfully pushed to switch {switch_id}.")
    else:
        print(f"Failed to push flow. Status code: {response.status_code}, Response: {response.text}")

# Function to retrieve all static flows
def get_static_flows():
    """
    Retrieve all static flows from the Floodlight controller.
    """
    url = f"{FLOODLIGHT_API_BASE}/wm/staticflowpusher/list/all/json"
    response = requests.get(url)
    if response.status_code == 200:
        flows = response.json()
        print("Current Static Flows:")
        print(json.dumps(flows, indent=4))
    else:
        print(f"Failed to retrieve flows. Status code: {response.status_code}, Response: {response.text}")

# Main Function
if __name__ == "__main__":
    # Example usage
    SWITCH_ID = "00:00:00:00:00:00:00:01"  # Replace with your switch DPID
    FLOW_NAME = "test-flow"
    IN_PORT = 1
    OUT_PORT = 2

    # Push a static flow
    push_static_flow(FLOW_NAME, SWITCH_ID, IN_PORT, OUT_PORT)

    # Retrieve and display all static flows
    get_static_flows()
