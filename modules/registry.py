from config import NODE_FILE

from modules.storage import load, save

from modules.wg_dump import dump as wg_dump

from logger import log

import time



def register(req):


    nodes = load(
        NODE_FILE,
        {}
    )


    wg_ip = req.get(
        "wg_ip"
    )


    if not wg_ip:

        return {
            "status":"error",
            "message":"missing wg_ip"
        }



    #
    # Lấy thông tin node từ wg0
    #

    wg_nodes = wg_dump()


    wg_info = wg_nodes.get(
        wg_ip
    )



    if not wg_info:


        log(
            "REGISTER WG NOT FOUND",
            wg_ip
        )


        return {

            "status":"error",

            "message":
                "wg peer not found"

        }



    old = nodes.get(
        wg_ip,
        {}
    )



    node = {

        "wg_ip":
            wg_ip,


        "role":
            req.get(
                "role",
                old.get(
                    "role",
                    "client"
                )
            ),


        "gateway_ip":
            req.get(
                "gateway_ip",
                old.get(
                    "gateway_ip"
                )
            ),


        "public_key":
            wg_info.get(
                "public_key"
            ),


        "endpoint":
            wg_info.get(
                "endpoint"
            ),


        "last_handshake":
            wg_info.get(
                "last_handshake",
                0
            ),


        "last_seen":
            int(
                time.time()
            )

    }



    nodes[wg_ip] = node



    save(
        NODE_FILE,
        nodes
    )



    log(
        "REGISTER",
        wg_ip,
        node
    )



    return {

        "status":
            "ok",


        "node":
            node

    }
