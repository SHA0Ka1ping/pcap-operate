import os
import sys
import socket
import select
import threading
import functools


class StdinSocket(threading.Thread):
    def __init__(self, detect_sock):
        threading.Thread.__init__(self)
        self.detect_sock = detect_sock

    def __del__(self):
        self.detect_sock.close()

    def run(self):
        stdin_fd = sys.stdin.fileno()
        while True:
            data = os.read(stdin_fd, 1024)
            if not data:
                print('StdinSocket closing')
                return
            self.detect_sock.send(data)


def getSockPair():
    socks_setup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks_setup.bind(('localhost', 8956))
    socks_setup.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks_setup.listen(1)

    stdin_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stdin_sock.connect(('localhost', 8956))
    detect_sock, _ = socks_setup.accept()
    socks_setup.close()
    stdin_sock.setblocking(False)
    detect_sock.setblocking(False)
    return stdin_sock, detect_sock


def getSdtinSock():
    stdin_sock, detect_sock = getSockPair()

    stdin_detector = StdinSocket(detect_sock)
    stdin_detector.start()
    return stdin_sock


def cmdStdSockReader(stdin_sock):
    cmd_data = stdin_sock.recv(1024).decode()
    # remove the '\r\n' at beginning or the end of cmd_data
    cmd_data = cmd_data.strip('\r\n')
    # remove the ' ' at beginning or the end of cmd_data
    cmd_data = cmd_data.strip(' ')

    # split cmd_data with '"'
    if cmd_data.count('"') % 2 != 0:
        print('Bad input, missing \'"\'')
        return False
    cmd_data = cmd_data.split('"')
    cmd_list = []
    for i, gadget in enumerate(cmd_data):
        if i % 2 == 1:
            cmd_list.append(gadget)
        else:
            # split cmd_data with ' '
            cmd_list.extend([word for word in gadget.split(' ')])
    # remove the '' from the list
    # FIXME if we actually don't want to split ' ' in a "'...'"
    cmd_list = [cmd for cmd in cmd_list if cmd != '']
    return cmd_list


def getStdinReader(stdin_sock):
    stdinReader = functools.partial(cmdStdSockReader, stdin_sock)
    return stdinReader


if __name__ == "__main__":
    stdin_sock = getSdtinSock()
    stdinReader = getStdinReader(stdin_sock)

    inputs = []
    outputs = []
    inputs.append(stdin_sock)

    while True:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)

        for reader in readable:
            if reader == stdin_sock:
                cmd_list = stdinReader()
                print(cmd_list)
