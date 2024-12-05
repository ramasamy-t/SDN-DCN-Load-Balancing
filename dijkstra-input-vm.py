import requests
import json
import numpy as np

# Replace with your Floodlight controller's IP address
CONTROLLER_IP = '127.0.0.1'
BASE_URL = f'http://{CONTROLLER_IP}:8080'

def enable_statistics():
    """
    Enable statistics collection on the Floodlight controller.
    """
    url = f'{BASE_URL}/wm/statistics/config/enable/json'
    response = requests.post(url, data='')
    if response.status_code == 200:
        print("Statistics collection enabled.")
    else:
        print(f"Failed to enable statistics collection: {response.status_code} {response.reason}")
        print(f"Response Content: {response.text}")

def get_switches():
    """
    Fetch all switches connected to the controller.
    """
    response = requests.get(f'{BASE_URL}/wm/core/controller/switches/json')
    return response.json()

def get_links():
    """
    Fetch the topology links between switches.
    """
    response = requests.get(f'{BASE_URL}/wm/topology/links/json')
    return response.json()

def get_bandwidth_stats(switch_id, port_id):
    """
    Fetch bandwidth statistics for a specific switch and port.
    """
    url = f'{BASE_URL}/wm/statistics/bandwidth/{switch_id}/{port_id}/json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching bandwidth stats for Switch {switch_id}, Port {port_id}: {response.status_code} {response.reason}")
        print(f"Response Content: {response.text}")
        return []


def print_links(links):
    """
    Print the links between switches in a readable format.
    :param links: List of links fetched from the controller.
    """
    print("\nLinks Between Switches:")
    for link in links:
        src_switch = link['src-switch']
        src_port = link['src-port']
        dst_switch = link['dst-switch']
        dst_port = link['dst-port']
        print(f"Source Switch: {src_switch} (Port: {src_port}) -> Destination Switch: {dst_switch} (Port: {dst_port})")

def print_bandwidth_stats(stats):
    """
    Print bandwidth statistics in a readable format.
    """
    print("\nBandwidth Statistics:")
    for stat in stats:
        print(f"Switch: {stat.get('dpid')}, Port: {stat.get('port')}, "
              f"RX (bps): {stat.get('bits-per-second-rx', 0)}, TX (bps): {stat.get('bits-per-second-tx', 0)}")

def get_static_flows(switch_id):
    """
    Fetch static flows for a specific switch or all switches.
    :param switch_id: Switch DPID or 'all'.
    :return: List of static flows.
    """
    url = f"{BASE_URL}/wm/staticflowpusher/list/{switch_id}/json"
    response = requests.get(url)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch flows for Switch {switch_id}: {response.status_code} {response.reason}")
        return {}

def print_flows(switch_id="all"):
    """
    Fetch and print all static flows for the specified switch or all switches.
    :param switch_id: Switch DPID or 'all'.
    """
    flows = get_static_flows(switch_id)
    print("\nStatic Flows:")
    for switch, flow_entries in flows.items():
        print(f"\nSwitch: {switch}")
        for flow_name, flow_details in flow_entries.items():
            print(f"  Flow Name: {flow_name}")
            for key, value in flow_details.items():
                print(f"    {key}: {value}")

def main():
    """
    Main function to enable statistics, fetch data, and process the network topology.
    """
    # Step 1: Enable statistics collection
    enable_statistics()

    # Step 2: Fetch switches and links
    switches = get_switches()
    print("\nSwitches:")
    for switch in switches:
        print(f"Switch DPID: {switch['switchDPID']}")
    links = get_links()
    print_links(links)

    print_flows('all')

    # Step 3: Prepare switch-to-index mapping
    switch_ids = {switch['switchDPID']: idx for idx, switch in enumerate(switches)}

    # Step 4: Fetch and print bandwidth statistics
    bandwidth_stats = []
    # print('Printing bandwidth')
    for switch in switches:
        dpid = switch['switchDPID']
        stats = get_bandwidth_stats(dpid, 'all')  # Fetch for all ports
        # print(stats)
        bandwidth_stats.extend(stats)

    print_bandwidth_stats(bandwidth_stats)


if __name__ == '__main__':
    main()
