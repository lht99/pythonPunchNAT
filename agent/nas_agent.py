#!/usr/bin/env python3

import json
import socket
import subprocess
import time
import os


BASE = os.path.dirname(
    os.path.abspath(__file__)
)

CONFIG = os.path.join(
    BASE,
    "config.json"
)

LOG = os.path.join(
    BASE,
    "logs",
    "agent.log"
)



def log(*args):

    os.makedirs(
        os.path.dirname(LOG),
        exist_ok=True
    )

    line = (
        time.strftime("%Y-%m-%d %H:%M:%S ")
        +
        " ".join(
            str(x) for x in args
        )
    )

    print(line)

    with open(
        LOG,
        "a"
    ) as f:

        f.write(
            line + "\n"
        )



def run(cmd):

    try:

        r = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        return r


    except Exception as e:

        log(
            "RUN ERROR",
            e
        )

        return None



def load_config():

    with open(
        CONFIG
    ) as f:

        return json.load(f)



def wg_show(interface):

    cmds = [

        f"wg show {interface}",

        f"sudo wg show {interface}"

    ]


    for c in cmds:

        r = run(c)

        if r and r.returncode == 0:

            return r.stdout


    return ""



def check_wg(cfg):

    interface = cfg.get(
        "interface",
        "wg5"
    )


    log(
        "CHECK WG",
        interface
    )


    out = wg_show(
        interface
    )


    if not out:

        log(
            "WG EMPTY"
        )

        return False



    log(out)



    if "peer:" not in out:

        return False


    return True



def check_forward():

    r = run(
        "sysctl -n net.ipv4.ip_forward"
    )


    return (
        r
        and
        r.stdout.strip()=="1"
    )



def enable_forward():

    log(
        "ENABLE FORWARD"
    )


    run(
        "sudo sysctl -w net.ipv4.ip_forward=1"
    )

def find_wan():

    r = run(
        "ip route | grep default"
    )


    if r and r.stdout:

        p = r.stdout.split()

        if "dev" in p:

            return p[
                p.index("dev") + 1
            ]


def setup_nat(cfg):

    wan = cfg.get(
        "wan_interface",
        "auto"
    )


    if wan == "auto":

        wan = find_wan()



    if not wan:

        log(
            "NO WAN"
        )

        return False



    log(
        "WAN",
        wan
    )


    subnet = "100.100.100.0/24"



    # =========================
    # FORWARD WG -> WAN
    # =========================

    forward_rule = [
        "sudo",
        "iptables",
        "-C",
        "FORWARD",
        "-i",
        "wg5",
        "-o",
        wan,
        "-j",
        "ACCEPT"
    ]


    r = subprocess.run(
        forward_rule,
        capture_output=True
    )


    if r.returncode != 0:

        log(
            "ADD FORWARD WG->WAN"
        )


        run(
            f"sudo iptables -A FORWARD "
            f"-i wg5 "
            f"-o {wan} "
            f"-j ACCEPT"
        )



    # =========================
    # FORWARD RETURN
    # =========================

    return_rule = [
        "sudo",
        "iptables",
        "-C",
        "FORWARD",
        "-i",
        wan,
        "-o",
        "wg5",
        "-m",
        "conntrack",
        "--ctstate",
        "RELATED,ESTABLISHED",
        "-j",
        "ACCEPT"
    ]


    r = subprocess.run(
        return_rule,
        capture_output=True
    )


    if r.returncode != 0:

        log(
            "ADD FORWARD WAN->WG"
        )


        run(
            f"sudo iptables -A FORWARD "
            f"-i {wan} "
            f"-o wg5 "
            f"-m conntrack "
            f"--ctstate RELATED,ESTABLISHED "
            f"-j ACCEPT"
        )



    # =========================
    # NAT MASQUERADE
    # =========================

    nat_rule = [
        "sudo",
        "iptables",
        "-t",
        "nat",
        "-C",
        "POSTROUTING",
        "-s",
        subnet,
        "-o",
        wan,
        "-j",
        "MASQUERADE"
    ]


    r = subprocess.run(
        nat_rule,
        capture_output=True
    )


    if r.returncode != 0:

        log(
            "ADD NAT",
            subnet,
            wan
        )


        run(
            f"sudo iptables -t nat -A POSTROUTING "
            f"-s {subnet} "
            f"-o {wan} "
            f"-j MASQUERADE"
        )

    else:

        log(
            "NAT EXISTS"
        )



    return True




def send_controller(data,cfg):


    host = cfg["controller"]

    port = int(
        cfg.get(
            "port",
            9000
        )
    )


    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )


    s.settimeout(
        10
    )


    s.connect(
        (
            host,
            port
        )
    )


    payload = (
        json.dumps(data)
        +
        "\n"
    )


    log(
        "SEND",
        payload
    )


    s.send(
        payload.encode()
    )


    result = s.recv(
        65535
    )


    s.close()


    return json.loads(
        result.decode()
    )





def register(cfg):


    data = {

        "cmd":
            "register",

        "wg_ip":
            cfg["wg_ip"],

        "role":
            "gateway"

    }


    return send_controller(
        data,
        cfg
    )





def apply_peer(peer,cfg):


    interface = cfg.get(
        "interface",
        "wg5"
    )


    key = peer.get(
        "public_key"
    )

    allowed = peer.get(
        "allowed_ips"
    )

    endpoint = peer.get(
        "endpoint"
    )


    if not key:

        return False



    cmd = (

        "sudo wg set "
        +
        interface
        +
        " peer "
        +
        key
        +
        " allowed-ips "
        +
        allowed

    )


    if endpoint:

        cmd += (
            " endpoint "
            +
            endpoint
        )


    cmd += (
        " persistent-keepalive 25"
    )


    log(
        "APPLY PEER",
        key,
        allowed,
        endpoint
    )


    r = run(
        cmd
    )


    if r and r.returncode == 0:

        log(
            "PEER APPLY OK"
        )

        return True



    log(
        "PEER APPLY FAIL",
        r.stderr if r else ""
    )


    return False

def gateway_sync(cfg):

    data = {

        "cmd":
            "gateway_sync",

        "wg_ip":
            cfg["wg_ip"]

    }


    result = send_controller(
        data,
        cfg
    )


    log(
        "GATEWAY SYNC RESPONSE",
        result
    )


    if result.get(
        "status"
    ) != "build":

        log(
            "SYNC FAILED"
        )

        return False



    peers = result.get(
        "peers",
        []
    )


    if not peers:

        log(
            "NO CLIENT PEERS"
        )

        return True



    for peer in peers:

        apply_peer(
            peer,
            cfg
        )



    return True





def main():

    cfg = load_config()


    log(
        "NAS AGENT START"
    )



    if not check_wg(cfg):

        log(
            "WG5 NOT READY"
        )

        return



    log(
        "WG5 READY"
    )



    if not check_forward():

        enable_forward()



    if not check_forward():

        log(
            "FORWARD FAIL"
        )

        return



    log(
        "FORWARD OK"
    )



    if not setup_nat(cfg):

        log(
            "NAT FAIL"
        )

        return



    log(
        "NAT OK"
    )



    result = register(
        cfg
    )


    log(
        "REGISTER RESPONSE",
        result
    )



    if result.get(
        "status"
    ) != "ok":

        log(
            "REGISTER FAILED"
        )

        return



    if gateway_sync(cfg):

        log(
            "GATEWAY READY"
        )

    else:

        log(
            "GATEWAY SYNC FAILED"
        )



    print(
        json.dumps(
            result,
            indent=2
        )
    )





if __name__ == "__main__":

    while True:

        try:

            main()

        except Exception as e:

            log(
                "MAIN ERROR",
                repr(e)
            )


        log(
            "WAIT 5s"
        )


        time.sleep(5)
