# Reproducing Dynamic Load Balancing in SDN-Based Data Center Networks

## Introduction

This repository provides a step-by-step guide to reproduce a dynamic load balancing mechanism in Software-Defined Networking (SDN) for data center networks. The implementation leverages Mininet for topology simulation and the Floodlight SDN controller for traffic management. The primary objective is to optimize traffic flow across a Fat-Tree topology, a widely-used hierarchical structure in data centers. By dynamically adapting to real-time network utilization, this solution effectively prevents congestion and improves bandwidth usage. Researchers and developers can use this repository to replicate the behavior, validate results, and analyze network performance.

## Goals

This project aims to reproduce the following:

1. A dynamic load balancing system for traffic optimization in SDN-based data center networks.
2. Efficient bandwidth utilization in a Fat-Tree topology by redistributing traffic based on real-time link utilization.
3. A scalable and adaptive SDN solution using the Floodlight controller and RESTful APIs for performance monitoring and management.

## Key Features

- **Fat-Tree Topology**: A scalable and hierarchical topology commonly used in data centers, implemented in Mininet.
- **Floodlight Controller**: Manages traffic flows, retrieves network statistics, and enforces dynamic routing policies.
- **Dynamic Load Balancing**: Continuously monitors link utilization and recomputes optimal paths every 10 seconds.
- **RESTful APIs**: Utilizes Floodlight APIs to fetch topology, bandwidth, and flow statistics and apply updated flow rules.
- **Traffic Engineering**: Ensures efficient bandwidth utilization by directing traffic based on real-time link statistics.

## Topology

Below is the Fat-Tree topology used for this project:

(![Fat Tree Topology](image.png))

## Steps to Implement and Verify Load Balancing

Execute steps 1, 2, 3, 5 before load balancing and collect results by following the verification steps listed below. Then, execute steps 1, 2, 3, 4, and 5 and collect results by following the same verification steps. This will indicate the change in bandwidth and distribution of traffic after the load balancing algorithm is applied.

### Steps:

1. **Start Mininet in Terminal 1**  
    ```bash
    docker exec -it mininet bash
    mn --custom /scripts/mininet-topology.py --topo customtopo --controller=remote,ip="floodlight"
    ```

2. **Collect TCP dump on Ethernet 1 of Switch 7**  
    Open a new terminal and run:  
    ```bash
    docker exec -it mininet bash
    tcpdump -i s7-eth2 -w s7-eth1.pcap &
    ```

3. **Collect TCP dump on Ethernet 2 of Switch 7**  
    Open another terminal and run:  
    ```bash
    tcpdump -i s7-eth1 -w s7-eth2.pcap &
    ```

4. **Start the Load Balancing Script**  
    Login to the Floodlight container and run:  
    ```bash
    docker exec -it floodlight bash
    python3 /scripts/loadbalancer.py
    ```

5. **Verify Traffic in Terminal 1**  
    ```bash
    mininet> h4 iperf -s &
    mininet> h1 iperf -c h4 -u -t 30 > h1_perf_output.txt &
    mininet> h2 iperf -c h4 -u -t 30 > h2_perf_output.txt &
    ```

## Results and Verification

1. **Traffic Distribution in Wireshark**  
    Import the `s7-eth1.pcap` and `s7-eth2.pcap` files into Wireshark. This will show the traffic distribution among the two interfaces of Switch 7.

2. **Change in Bandwidth**  
    Open the files `h1_perf_output.txt` and `h2_perf_output.txt` to see the changes in bandwidth before and after applying the load balancing algorithm.