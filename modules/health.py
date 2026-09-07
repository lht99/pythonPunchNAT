from modules.topology import build



def health():

    topo=build()


    return {

        "status":
        "ok",

        "nodes":
        len(topo)

    }
