# modules/plan.py


from logger import log





def normalize_peer(peer):

    """
    Chuẩn hóa peer để so sánh

    """

    if not peer:

        return None



    return {

        "PublicKey":
            peer.get(
                "PublicKey",
                peer.get(
                    "public_key"
                )
            ),


        "AllowedIPs":
            peer.get(
                "AllowedIPs",
                peer.get(
                    "allowed_ips"
                )
            ),


        "Endpoint":
            peer.get(
                "Endpoint",
                peer.get(
                    "endpoint"
                )
            ),


        "PersistentKeepalive":
            peer.get(
                "PersistentKeepalive",
                peer.get(
                    "persistent_keepalive",
                    "21"
                )
            )

    }





def peer_key(peer):


    return peer.get(
        "PublicKey"
    )





def compare_peer(
        old,
        new
):


    changes=[]


    fields=[

        "AllowedIPs",

        "Endpoint",

        "PersistentKeepalive"

    ]


    for field in fields:


        if old.get(field) != new.get(field):

            changes.append(
                field
            )


    return changes





def make_plan(
        current_peers,
        desired_peers
):


    """
    current_peers:
        lấy từ wg showconf


    desired_peers:
        server sync_builder trả về

    """


    current={}


    desired={}



    for peer in current_peers:


        p=normalize_peer(
            peer
        )


        if p.get(
            "PublicKey"
        ):

            current[
                p["PublicKey"]
            ]=p





    for peer in desired_peers:


        p=normalize_peer(
            peer
        )


        if p.get(
            "PublicKey"
        ):

            desired[
                p["PublicKey"]
            ]=p





    add=[]

    update=[]

    remove=[]




    #
    # ADD
    #

    for key,peer in desired.items():


        if key not in current:


            add.append(
                peer
            )



    #
    # UPDATE
    #

    for key,old in current.items():


        if key in desired:


            new=desired[key]


            changes=compare_peer(
                old,
                new
            )


            if changes:


                update.append({

                    "public_key":
                        key,


                    "changes":
                        changes,


                    "old":
                        old,


                    "new":
                        new

                })




    #
    # REMOVE
    #

    for key,peer in current.items():


        if key not in desired:


            remove.append(
                peer
            )




    result={


        "status":
            "plan",


        "interface_changed":
            False,


        "add":
            add,


        "update":
            update,


        "remove":
            remove,


        "summary":{

            "add":
                len(add),


            "update":
                len(update),


            "remove":
                len(remove)

        },


        "apply_required":
            bool(
                add or update or remove
            )

    }



    log(
        "PLAN",
        result
    )


    return result
