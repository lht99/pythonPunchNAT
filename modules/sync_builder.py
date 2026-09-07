import time
from modules.storage import load


NODE_FILE = "data/nodes.json"


def load_nodes():

    return load(
        NODE_FILE,
        {}
    )



def build_client(wg_ip):

    nodes = load_nodes()

    client = nodes.get(wg_ip)

    if not client:
        return {
            "status": "error",
            "error": "client_not_found"
        }

    gateway_ip = client.get("gateway_ip")

    if not gateway_ip:
        return {
            "status": "error",
            "error": "no_gateway"
        }

    gateway = nodes.get(gateway_ip)

    if not gateway:
        return {
            "status": "error",
            "error": "gateway_not_found"
        }


    peer = {
        "public_key": gateway.get(
            "public_key"
        ),
        "allowed_ips": gateway_ip + "/32",
        "endpoint": gateway.get(
            "endpoint"
        )
    }


    return {
        "status": "build",
        "role": "client",
        "wg_ip": wg_ip,
        "peers": [
            peer
        ]
    }



def build_gateway(wg_ip):

    nodes = load_nodes()

    peers = []


    for ip,node in nodes.items():

        if node.get(
            "gateway_ip"
        ) == wg_ip:


            peers.append(
                {
                    "public_key": node.get(
                        "public_key"
                    ),

                    "allowed_ips":
                        ip + "/32",

                    "endpoint":
                        node.get(
                            "endpoint"
                        )
                }
            )


    return {
        "status":"build",
        "role":"gateway",
        "wg_ip":wg_ip,
        "peers":peers
    }



def build_gateway_sync(wg_ip):

    result = build_gateway(
        wg_ip
    )

    result["cmd"]="gateway_sync"

    result["time"]=int(
        time.time()
    )

    return result
def build(req):

    wg_ip = req.get(
        "wg_ip"
    )

    nodes = load_nodes()


    node = nodes.get(
        wg_ip
    )


    if not node:

        return {
            "status":"error",
            "error":"node_not_found"
        }



    if node.get(
        "role"
    ) == "gateway":

        return build_gateway(
            wg_ip
        )


    return build_client(
        wg_ip
    )
