# WireGuard Gateway Agent

A lightweight WireGuard management agent for automatic gateway registration, peer synchronization, and NAT gateway setup.

This agent works together with **WireGuard Dynamic Gateway Controller**.

The agent runs on gateway/client nodes and communicates with the controller to automatically maintain WireGuard peer configuration.

---

# Features

## Node Registration

Automatically registers the node with the controller.

Example:

```json
{
    "cmd": "register",
    "wg_ip": "100.100.100.100",
    "role": "gateway"
}
```

The controller stores:

- WireGuard IP
- Node role
- Public key
- Endpoint
- Handshake status


---

## Gateway Synchronization

Gateway nodes periodically request updated peer information.

Flow:

```
Agent
  |
  | gateway_sync
  |
Controller
  |
  | peer list
  |
Agent
  |
  | apply changes
  |
WireGuard
```

The agent automatically:

- compares existing peers
- detects new peers
- detects changed endpoints
- applies required changes only


---

## WireGuard Health Check

Before registering, the agent checks:

- WireGuard interface exists
- Peer exists
- Latest handshake available


Example:

```
CHECK WG wg5

WG READY
```

---

## IP Forwarding

For gateway mode, the agent verifies:

```
net.ipv4.ip_forward
```

If disabled:

```
ENABLE FORWARD
```

The agent enables:

```
net.ipv4.ip_forward=1
```

---

## NAT Gateway

Gateway nodes can provide internet access for WireGuard clients.

Example:

```
Client
  |
WireGuard
  |
Gateway
  |
eth0
  |
Internet
```

The agent automatically creates:

```bash
iptables -t nat \
-A POSTROUTING \
-s 100.100.100.0/24 \
-o eth0 \
-j MASQUERADE
```

---

# Architecture

```
                    Controller VPS

                         |
                         |
                    TCP API 9000

                         |

                 WireGuard Agent

                         |

              +-------------------+
              |                   |
          Gateway Node        Client Node

       100.100.100.100     100.100.100.x

```

---

# Supported Roles


## Gateway

Gateway nodes provide:

- NAT forwarding
- peer routing
- internet access


Example:

```json
{
    "wg_ip":"100.100.100.100",
    "role":"gateway"
}
```


---

## Client

Client nodes connect through gateway.


Example:

```json
{
    "wg_ip":"100.100.100.5",
    "role":"client",
    "gateway_ip":"100.100.100.100"
}
```


---

# Directory Structure

```
agent/

├── nas_agent.py

├── install.sh

├── config.json

├── logs/

│   └── agent.log

└── README.md

```

---

# Installation


## Requirements

Supported:

- Synology NAS
- Ubuntu
- Debian
- Linux gateway systems


Requirements:

```
Python 3.8+
WireGuard
iptables
sudo privilege
```


---

# Install

Copy agent files:

```
/docker/agent/
```

Run:

```bash
chmod +x install.sh

./install.sh
```

Example output:

```
Install NAS Gateway Agent

Done
```

---

# Configuration


Create:

```
config.json
```


Example:

```json
{
    "controller":"Your_server_IP",

    "port":9000,

    "wg_ip":"100.100.100.100",

    "role":"gateway",

    "interface":"wg5",

    "wan_interface":"auto",

    "apply_nat":true
}
```


---

# Configuration Parameters


## controller

Controller server IP address.

Example:

```json
"controller":"1.2.3.4"
```


---

## port

Controller API port.

Default:

```
9000
```


---

## wg_ip

WireGuard address of this node.

Example:

```
100.100.100.100
```


---

## role

Node type:

Gateway:

```json
"role":"gateway"
```

Client:

```json
"role":"client"
```


---

## interface

WireGuard interface name.

Example:

```json
"interface":"wg5"
```


---

## wan_interface

Internet interface.

Automatic detection:

```json
"wan_interface":"auto"
```

Manual:

```json
"wan_interface":"eth0"
```


---

## apply_nat

Enable NAT configuration.

Enable:

```json
"apply_nat":true
```

Disable:

```json
"apply_nat":false
```


---

# Running Agent


Manual:

```bash
python3 nas_agent.py
```


Example output:

```
NAS AGENT START

CHECK WG wg5

WG READY

FORWARD OK

WAN eth0

NAT OK

REGISTER RESPONSE

GATEWAY SYNC RESPONSE

PEER APPLY OK

GATEWAY READY
```


---

# Background Running


Example:

```bash
nohup python3 nas_agent.py \
> logs/agent.log 2>&1 &
```


Check:

```bash
ps aux | grep nas_agent
```


Stop:

```bash
kill $(cat nas_agent.pid)
```


---

# Runtime Flow


Every synchronization cycle:


```
1. Start agent

        |

2. Check WireGuard status

        |

3. Enable forwarding if needed

        |

4. Setup NAT

        |

5. Register node

        |

6. Request gateway_sync

        |

7. Compare peer list

        |

8. Apply changed peers

        |

9. Write log

```


---

# Logs


Location:

```
logs/agent.log
```


Example:

```
2026-09-07 06:59:58 NAS AGENT START

CHECK WG wg5

WG READY

FORWARD OK

NAT OK

REGISTER RESPONSE

GATEWAY READY
```


---

# Security


Do not publish:

```
config.json

logs/agent.log

WireGuard private keys

Production endpoints
```


For public repositories use:

```
config.example.json
```


---

# Troubleshooting


## WG not ready

Check:

```bash
sudo wg show wg5
```


---

## NAT not working

Check:

```bash
sysctl net.ipv4.ip_forward
```

Expected:

```
net.ipv4.ip_forward = 1
```


Check:

```bash
sudo iptables -t nat -L POSTROUTING
```


---

## Controller unreachable

Test:

```bash
nc YOUR_SERVER_IP 9000
```


---

# Project Status

Current version:

```
Experimental Release
```


Tested:

- Synology NAS gateway
- Ubuntu gateway
- WireGuard wg5
- NAT forwarding
- Automatic peer synchronization
- Remote RDP access


---

# License

Choose a license before public release.

Recommended:

MIT License
