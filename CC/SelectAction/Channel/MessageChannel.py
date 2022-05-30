from enum import Enum, auto
from socket import socket
from hashlib import md5 as getHash
from typing import Tuple
from SelectAction.base.KeyAgreement import keyAgreementServer, keyAgreementClient

PACKAGE_LEN = 2048


class _Pipe():
    def __init__(self, pipeIN, pipeOUT) -> None:
        self.pipeIN = pipeIN
        self.pipeOUT = pipeOUT

    def recv(self):
        return self.pipeIN()

    def send(self, package):
        return self.pipeOUT(package)


class _Package():
    MSG_ID_LEN = 32

    def __init__(self, message: str) -> None:
        message_hash = getHash(message.encode()).hexdigest()
        self.hash_id = message_hash[:_Package.MSG_ID_LEN]

    def encode(self, segment: str):
        return self.hash_id + segment

    @staticmethod
    def decode(package: str):
        return {
            'hash_id': package[:_Package.MSG_ID_LEN],
            'segment': package[_Package.MSG_ID_LEN:],
        }


class SendState(Enum):
    SENDING = auto()
    SENDALL = auto()


class RecvState(Enum):
    RECVING = auto()
    RECVALL = auto()


class MessageChannel():
    def __init__(self, channel_socket: socket, if_raiser: bool) -> None:
        self.socket = channel_socket
        if if_raiser:
            pipe_pair = keyAgreementServer(channel_socket)
        else:
            pipe_pair = keyAgreementClient(channel_socket)
        self.pipe = _Pipe(*pipe_pair)
        self.recving_dict = {}

    def send(self, message: str) -> Tuple[SendState, int]:
        def messageSendTask():
            packager = _Package(message)
            for segment in [message[i:i+PACKAGE_LEN]
                            for i in range(0, len(message), PACKAGE_LEN)]:
                send_cnt = self.pipe.send(packager.encode(segment))
                state = SendState.SENDING
                # print(segment)
                yield state, send_cnt
            send_cnt = self.pipe.send(packager.encode(''))
            state = SendState.SENDALL
            yield state, send_cnt
        return messageSendTask

    def read(self) -> Tuple[RecvState, str, str]:
        content = self.pipe.recv()
        package = _Package.decode(content)

        if package['hash_id'] not in self.recving_dict:
            self.recving_dict[package['hash_id']] = ''
        segment_message = package['segment']
        self.recving_dict[package['hash_id']] += segment_message

        current_message = self.recving_dict[package['hash_id']]

        if package['segment'] == '':
            state = RecvState.RECVALL
            self.recving_dict.pop(package['hash_id'])
        else:
            state = RecvState.RECVING

        return state, segment_message, current_message
