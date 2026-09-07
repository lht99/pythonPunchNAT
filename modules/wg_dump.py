import subprocess

from logger import log



def dump():

    peers = {}


    try:

        result = subprocess.run(
            [
                "wg",
                "show",
                "wg0",
                "dump"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )


        if result.returncode != 0:

            log(
                "WG_DUMP ERROR",
                result.stderr
            )

            return peers



        lines = result.stdout.strip().splitlines()


        if len(lines) <= 1:

            return peers



        for line in lines[1:]:


            fields = line.split("\t")


            if len(fields) < 5:

                continue



            public_key = fields[0].strip()


            endpoint = fields[2].strip()


            allowed_ips = fields[3].strip()


            handshake = fields[4].strip()



            if endpoint == "(none)":

                endpoint = None



            try:

                handshake = int(
                    handshake
                )

            except:

                handshake = 0



            #
            # allowed_ips:
            # 100.100.100.x/32
            #

            for ip in allowed_ips.split(","):


                ip = ip.strip()


                if ip.endswith("/32"):


                    wg_ip = ip.replace(
                        "/32",
                        ""
                    )


                    peers[wg_ip] = {

                        "wg_ip":
                            wg_ip,


                        "public_key":
                            public_key,


                        "endpoint":
                            endpoint,


                        "last_handshake":
                            handshake

                    }



        log(
            "WG_DUMP",
            peers
        )


    except Exception as e:


        log(
            "WG_DUMP EXCEPTION",
            repr(e)
        )



    return peers
