# Dynamic WireGuard Gateway Controller

A lightweight self-hosted controller for managing dynamic WireGuard peers, gateway synchronization, and NAT-based remote access networks.

This project provides a simple control plane on top of WireGuard to automatically register nodes, maintain peer information, and synchronize gateway peer configurations.

---

## Features

- Automatic WireGuard node registration
- Dynamic peer discovery
- Gateway-based network topology
- Automatic gateway peer synchronization
- Centralized node registry
- WireGuard status monitoring
- NAT gateway support
- Remote access through WireGuard overlay network
- Designed for NAS, Windows clients, VPS gateways

---

# Architecture

```
                 Controller VPS
               (Control Plane)
                      |
                      |
              register / sync API
                      |
                      |
              +----------------+
              |  Gateway Node  |
              |  WireGuard wg5 |
              | 100.100.100.100|
              +----------------+
                 /     |      \
                /      |       \
               /       |        \
        Client .2   Client .5   Client .6

        100.100.100.x Overlay Network
```

The controller does not forward traffic.

It only manages:

- node registration
- peer information
- gateway synchronization

Actual traffic is handled by WireGuard.

---

# Components

## Controller

Runs on Linux VPS.

Responsibilities:

- Receive node registration
- Store node information
- Generate synchronization plans
- Monitor WireGuard peers
- Provide health information


Main file:

```
server.py
```

---

## Agent

Runs on gateway/client devices.

Responsibilities:

- Check WireGuard status
- Register node
- Request gateway synchronization
- Apply peer changes
- Report status

Supported environments:

- Linux
- NAS
- Windows (planned/implemented separately)

---

# Directory Structure

```
controller/

├── server.py
├── config.py
├── logger.py
│
├── modules/
│   ├── storage.py
│   ├── registry.py
│   ├── wg_dump.py
│   ├── sync_builder.py
│   ├── health.py
│   ├── topology.py
│   ├── rules.py
│   ├── plan.py
│   ├── apply.py
│   └── sync_file.py
│
└── data/
    └── nodes.json
```

---

# Network Design

Default WireGuard overlay:

```
100.100.100.0/24
```

Example:

```
Controller:
100.100.100.1

Gateway:
100.100.100.100

Client:
100.100.100.5
100.100.100.6
```

---

# Node Registration

A node registers with:

```json
{
    "cmd": "register",
    "wg_ip": "100.100.100.5",
    "role": "client",
    "gateway_ip": "100.100.100.100"
}
```

The controller stores:

- WireGuard public key
- Endpoint
- Node role
- Gateway relationship
- Last handshake status

---

# Gateway Synchronization

Gateway nodes request:

```json
{
    "cmd": "gateway_sync",
    "wg_ip": "100.100.100.100"
}
```

Controller returns:

```json
{
    "status": "build",
    "role": "gateway",
    "wg_ip": "100.100.100.100",
    "peers": [
        {
            "public_key": "CLIENT_PUBLIC_KEY",
            "allowed_ips": "100.100.100.5/32",
            "endpoint": "CLIENT_ENDPOINT"
        }
    ]
}
```

The agent applies the required peer configuration.

---

# Runtime Flow

```
1. Node starts
        |
        v
2. Check WireGuard
        |
        v
3. Register to controller
        |
        v
4. Controller updates node database
        |
        v
5. Gateway requests sync
        |
        v
6. Peer list generated
        |
        v
7. Agent applies changes
```

---

# Installation

## Requirements

- Python 3.10+
- WireGuard
- Linux system
- TCP port 9000 open for controller API


Install:

```bash
git clone <repository>

cd controller
```

---

## Configure

Create:

```
config.py
```

Example:

```python
HOST = "0.0.0.0"
PORT = 9000

NODE_FILE = "data/nodes.json"
```

---

## Run Controller

```bash
python3 server.py
```

Example:

```
Controller listen 9000
```

---

# Database

Runtime database:

```
data/nodes.json
```

Example:

```json
{}
```

Do not commit production node databases.

Use:

```
nodes.example.json
```

for public repositories.

---

# Security Notes

Before publishing:

Remove:

- Private keys
- Real public IP addresses
- Endpoint information
- Production node database
- Logs

Never publish:

```
PrivateKey =
```

WireGuard private keys.

---

# WireGuard Dynamic Gateway Controller

A self-hosted WireGuard controller and gateway synchronization system.

This project contains two main components:

- Controller
- Agent


---

# Components


## 1. Controller

The controller manages:

- Node registration
- Peer registry
- Gateway synchronization
- WireGuard topology
- Health status


Location:


# Roadmap

Future development:

- Web dashboard
- Client approval system
- Automatic gateway selection
- Rule engine
- Policy-based routing
- Multi-gateway support
- Node health monitoring
- Automatic failover

---

# Project Status

Current version:

**Experimental / Self-hosted deployment**

Tested:

- VPS controller
- NAS gateway
- Multiple WireGuard clients
- NAT traversal
- Remote RDP access
- Gateway peer synchronization

---

# License

Choose a license before public release.

Recommended:

MIT License
