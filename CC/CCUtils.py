import socket

from CCConfig import *


def createUnblockedlistener(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.listen(MAX_WAITING)
    listener.setblocking(False)

    return listener


def createUnblockedConnection(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    connection.setblocking(False)

    return connection
