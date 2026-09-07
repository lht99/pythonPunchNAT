from logger import log



def build_interface(interface):

    lines=[]

    lines.append(
        "[Interface]"
    )


    for key,value in interface.items():

        lines.append(
            f"{key} = {value}"
        )


    return "\n".join(lines)





def build_peer(peer):

    lines=[]


    lines.append(
        "[Peer]"
    )


    if peer.get("public_key"):

        lines.append(
            "PublicKey = " +
            peer["public_key"]
        )


    if peer.get("allowed_ips"):

        lines.append(
            "AllowedIPs = " +
            peer["allowed_ips"]
        )


    if peer.get("endpoint"):

        lines.append(
            "Endpoint = " +
            peer["endpoint"]
        )


    lines.append(
        "PersistentKeepalive = 21"
    )


    return "\n".join(lines)





def build_sync_conf(
        interface,
        peers
):


    blocks=[]


    blocks.append(
        build_interface(
            interface
        )
    )



    for peer in peers:

        blocks.append(

            build_peer(
                peer
            )

        )



    conf="\n\n".join(
        blocks
    )


    log(
        "SYNC CONF GENERATED"
    )


    log(
        conf
    )


    return conf
