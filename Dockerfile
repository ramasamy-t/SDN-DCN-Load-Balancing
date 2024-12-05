# Use the existing Floodlight image as the base
FROM piyushk2001/floodlight-controller:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install additional tools and dependencies
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    python3 \
    python3-pip && \
    pip3 install --no-cache-dir \
    networkx \
    requests

# Expose necessary ports
EXPOSE 6653
EXPOSE 8080