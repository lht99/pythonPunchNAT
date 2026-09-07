from config import NODE_FILE
from modules.storage import load
from logger import log



def get_nodes():

    return load(
        NODE_FILE,
        {}
    )





def build(nodes=None):

    """
    Build topology từ nodes.json

    """

    if nodes is None:

        nodes = get_nodes()


    topology={}


    for ip,node in nodes.items():

        topology[ip]=node.copy()



    log(
        "TOPOLOGY",
        topology
    )


    return topology





def get_node(
        wg_ip,
        topology=None
):

    if topology is None:

        topology=build()



    return topology.get(
        wg_ip
    )





def find_gateway(
        topology,
        client_ip=None,
        gateway_ip=None
):


    #
    # ưu tiên gateway được chỉ định
    #

    if gateway_ip:


        gw=topology.get(
            gateway_ip
        )


        if gw and gw.get(
            "role"
        )=="gateway":

            return gw



    #
    # lấy từ client record
    #

    if client_ip:


        client=topology.get(
            client_ip
        )


        if client:


            gid=client.get(
                "gateway_ip"
            )


            if gid:


                gw=topology.get(
                    gid
                )


                if gw and gw.get(
                    "role"
                )=="gateway":

                    return gw



    #
    # Không tự chọn gateway
    #
    # tránh client nhảy về gateway cũ
    #

    return None





def gateway_clients(
        topology,
        gateway_ip
):


    result=[]


    for ip,node in topology.items():


        if node.get(
            "role"
        )!="client":

            continue



        if node.get(
            "gateway_ip"
        ) == gateway_ip:


            result.append(
                node
            )


    return result





def gateways(
        topology
):


    result=[]


    for node in topology.values():

        if node.get(
            "role"
        )=="gateway":

            result.append(
                node
            )


    return result
