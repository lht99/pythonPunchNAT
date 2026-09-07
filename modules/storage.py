import json
import os


def load(path,default):

    if not os.path.exists(path):
        return default


    try:

        with open(path) as f:
            return json.load(f)

    except:

        return default



def save(path,data):

    with open(path,"w") as f:

        json.dump(
            data,
            f,
            indent=2
        )
