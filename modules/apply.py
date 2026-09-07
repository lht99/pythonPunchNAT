# modules/apply.py


from logger import log





def build_apply(
        interface,
        plan,
        sync_file
):


    if not plan:

        return {

            "status":"error",

            "message":
                "missing plan"

        }



    if not plan.get(
        "apply_required",
        False
    ):


        result={

            "status":
                "nothing_to_apply"

        }


        log(
            "APPLY",
            result
        )


        return result





    result={


        "status":
            "apply_ready",


        "action":
            "syncconf",


        "interface":
            interface,


        "file":
            sync_file,


        "changes":{

            "add":
                len(
                    plan.get(
                        "add",
                        []
                    )
                ),


            "update":
                len(
                    plan.get(
                        "update",
                        []
                    )
                ),


            "remove":
                len(
                    plan.get(
                        "remove",
                        []
                    )
                )

        }

    }


    log(
        "APPLY READY",
        result
    )


    return result





def apply(
        interface,
        plan,
        sync_file
):

    return build_apply(
        interface,
        plan,
        sync_file
    )
