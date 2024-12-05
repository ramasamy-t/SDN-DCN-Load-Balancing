import requests
import json
import time
import networkx as nx

# Floodlight REST API Base URL
FLOODLIGHT_REST_API = "http://localhost:8080"

# Fetch Network Topology
def fetch_network_topology():
    try:
        response = requests.get(f"{FLOODLIGHT_REST_API}/wm/topology/links/json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching network topology: {e}")
        return []

# Fetch Bandwidth Stats for Specific Switch and Port
def fetch_bandwidth_stats(switch_id, port_id):
    try:
        response = requests.get(f"{FLOODLIGHT_REST_API}/wm/statistics/bandwidth/{switch_id}/{port_id}/json")
        response.raise_for_status()
        stats = response.json()
        return stats[0] if stats else {}
    except requests.RequestException as e:
        print(f"Error fetching bandwidth stats for Switch {switch_id}, Port {port_id}: {e}")
        return {}

# Fetch Bandwidth Stats for All Links
def fetch_link_stats(topology):
    link_utilization = {}
    for link in topology:
        src_switch = link['src-switch']
        src_port = link['src-port']
        stats = fetch_bandwidth_stats(src_switch, src_port)
        if stats:
            link_utilization[(src_switch, src_port)] = stats.get('bits-per-second-tx', 0)
    return link_utilization

# Push Static Flow
def push_flow(flow_name, switch_id, in_port, out_port, priority=1000):
    flow = {
        "switch": switch_id,
        "name": flow_name,
        "priority": str(priority),
        "eth_type": "0x0800",  # IPv4
        "in_port": str(in_port),
        "active": "true",
        "actions": f"output={out_port}"
    }
    try:
        response = requests.post(
            f"{FLOODLIGHT_REST_API}/wm/staticflowpusher/json",
            data=json.dumps(flow),
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"Flow '{flow_name}' successfully pushed to switch {switch_id}.")
        else:
            print(f"Failed to push flow '{flow_name}': {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Error pushing flow '{flow_name}': {e}")

# Build Network Graph
def build_network_graph(topology, link_utilization):
    graph = nx.DiGraph()
    for link in topology:
        src_switch = link['src-switch']
        src_port = link['src-port']
        dst_switch = link['dst-switch']
        dst_port = link['dst-port']
        weight = link_utilization.get((src_switch, src_port), 1)  # Use utilization as weight
        graph.add_edge(src_switch, dst_switch, weight=weight, src_port=src_port, dst_port=dst_port)
    return graph

# Compute Optimal Paths and Push Flows
def update_flows(graph, traffic_matrix):
    for flow in traffic_matrix:
        src = flow['src']
        dst = flow['dst']
        if nx.has_path(graph, src, dst):
            path = nx.shortest_path(graph, source=src, target=dst, weight='weight')
            for i in range(len(path) - 1):
                src_switch = path[i]
                dst_switch = path[i + 1]
                src_port = graph[src_switch][dst_switch]['src_port']
                dst_port = graph[src_switch][dst_switch]['dst_port']
                flow_name = f"flow-{src}-{dst}-{i}"
                push_flow(flow_name, src_switch, src_port, dst_port)

# Main Function
def main():
    while True:
        print("\n--- Fetching Network State ---")
        # Step 1: Fetch network topology
        topology = fetch_network_topology()
        if not topology:
            print("Failed to retrieve topology. Retrying in 10 seconds.")
            time.sleep(10)
            continue
        print(topology)


        # Step 2: Fetch link utilization stats
        link_utilization = fetch_link_stats(topology)
        if not link_utilization:
            print("Link is not used, collecting stats. Retrying in 10 seconds.")
            time.sleep(10)
            continue
        print(link_utilization)

        # Step 3: Build network graph
        graph = build_network_graph(topology, link_utilization)

        # Step 4: Define traffic matrix (example)
        traffic_matrix = [
            {"src": "00:00:00:00:00:00:00:07", "dst": "00:00:00:00:00:00:00:08"},
            {"src": "00:00:00:00:00:00:00:03", "dst": "00:00:00:00:00:00:00:04"}
        ]

        # Step 5: Update flows based on optimal paths
        print("\n--- Updating Flows ---")
        update_flows(graph, traffic_matrix)

        # Step 6: Wait for the next monitoring cycle
        print("\n--- Monitoring Complete. Waiting 10 seconds ---")
        time.sleep(10)

if __name__ == "__main__":
    main()