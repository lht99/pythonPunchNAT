import datetime


def log(*msg):

    text=datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print(
        text,
        *msg,
        flush=True
    )
