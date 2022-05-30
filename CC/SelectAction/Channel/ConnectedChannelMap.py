from socket import socket
from typing import Dict
from hashlib import md5 as getHash

from SelectAction.Channel.MessageChannel import MessageChannel
from SelectAction.base.ConnectionNotFound import ConnectionNotFound


class ConnectedChannelMap:
    def __init__(self) -> None:
        self.name_map: Dict[socket, str] = {}
        self.connect_map: Dict[str, MessageChannel] = {}

    def __iter__(self):
        return iter(list(self.connect_map.keys()))

    def addChannel(self, socket_connection: socket, message_channel: MessageChannel):
        socket_name = getHash(
            hex(hash(socket_connection)).encode()).hexdigest()
        self.name_map[socket_connection] = socket_name
        print(self.name_map)
        self.connect_map[socket_name] = message_channel

    def getChannel(self, socket_identity: object) -> MessageChannel:
        try:
            if isinstance(socket_identity, str):
                # socket_identity is the name generate for socket
                socket_name = socket_identity
            elif isinstance(socket_identity, socket):
                # socket_identity is socket itself
                socket_name = self.name_map[socket_identity]
            return self.connect_map[socket_name]
        except KeyError:
            raise ConnectionNotFound

    def delChannel(self, socket_identity: object):
        if isinstance(socket_identity, str):
            # socket_identity is the name generate for socket
            socket_name = socket_identity
            if socket_name not in self.connect_map:
                return False
            socket_connection = self.connect_map[socket_name].socket
        elif isinstance(socket_identity, socket):
            # socket_identity is socket itself
            socket_connection = socket_identity
            if socket_connection not in self.name_map:
                return False
            socket_name = self.name_map[socket_connection]
        self.name_map.pop(socket_connection)
        self.connect_map.pop(socket_name)
        return True
