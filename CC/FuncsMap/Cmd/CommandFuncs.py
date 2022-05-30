import sys
from CCDaemon import CCDaemon


def show(argv: str):
    print(argv.split(' ', maxsplit=1)[1])
    sys.exit(0)
