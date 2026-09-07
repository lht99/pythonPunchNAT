import socket
import json
import time
import traceback


from config import HOST, PORT, NODE_FILE

from modules.storage import load, save
from modules.registry import register
from modules.sync_builder import (
    build,
    build_gateway_sync
)
from modules.wg_dump import dump as wg_dump

from logger import log



def refresh_nodes():

    nodes = load(
        NODE_FILE,
        {}
    )


    wg_nodes = wg_dump()


    changed = False



    for wg_ip, wg_info in wg_nodes.items():


        if wg_ip in nodes:


            node = nodes[wg_ip]


            if (
                node.get("public_key")
                !=
                wg_info.get("public_key")
                or

                node.get("endpoint")
                !=
                wg_info.get("endpoint")
                or

                node.get("last_handshake")
                !=
                wg_info.get("last_handshake")
            ):


                node["public_key"] = wg_info.get(
                    "public_key"
                )


                node["endpoint"] = wg_info.get(
                    "endpoint"
                )


                node["last_handshake"] = wg_info.get(
                    "last_handshake",
                    0
                )


                changed = True



    if changed:

        save(
            NODE_FILE,
            nodes
        )


    return nodes





def handle(req):


    cmd = req.get(
        "cmd"
    )


    log(
        "CMD",
        cmd
    )



    if cmd == "register":


        return register(
            req
        )



    elif cmd == "sync":


        refresh_nodes()


        return build(
            req
        )



    elif cmd == "gateway_sync":


        refresh_nodes()


        return build_gateway_sync(
            req.get(
                "wg_ip"
            )
        )



    elif cmd == "nodes":


        refresh_nodes()


        return {


            "status":
                "ok",


            "nodes":
                load(
                    NODE_FILE,
                    {}
                )

        }



    elif cmd == "health":


        return {


            "status":
                "ok",


            "nodes":
                len(
                    load(
                        NODE_FILE,
                        {}
                    )
                ),


            "time":
                int(
                    time.time()
                )

        }



    return {


        "status":
            "error",


        "message":
            "unknown command"

    }

def serve():


    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )


    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )


    s.bind(
        (
            HOST,
            PORT
        )
    )


    s.listen(
        50
    )


    log(
        f"Controller listen {PORT}"
    )



    while True:


        conn, addr = s.accept()


        try:


            data = conn.recv(
                65535
            )


            if not data:


                conn.close()

                continue



            try:


                text = data.decode(
                    "utf-8"
                )


            except UnicodeDecodeError:


                log(
                    "INVALID BINARY REQUEST",
                    addr,
                    data[:32]
                )


                conn.close()

                continue



            try:


                req = json.loads(
                    text
                )


            except json.JSONDecodeError:


                log(
                    "INVALID JSON",
                    addr,
                    text[:100]
                )


                conn.close()

                continue



            log(
                "REQUEST",
                addr,
                req
            )



            result = handle(
                req
            )


            log(
                "RESPONSE",
                result
            )


            conn.send(
                json.dumps(
                    result
                ).encode()
            )



        except Exception as e:


            log(
                "HANDLER ERROR",
                repr(e)
            )


            traceback.print_exc()



        finally:


            conn.close()





if __name__ == "__main__":


    serve()

