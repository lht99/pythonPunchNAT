from config import RULE_FILE
from modules.storage import load



def get():

    return load(
        RULE_FILE,
        {}
    )
