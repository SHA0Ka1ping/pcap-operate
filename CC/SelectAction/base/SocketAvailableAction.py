from socket import socket
from abc import ABC, abstractclassmethod

from SelectAction.Channel.MessageChannel import MessageChannel


class SocketAvailableAction(ABC):

    def __init__(self, socket: socket) -> None:
        self.socket = socket

    @abstractclassmethod
    def availableAction(self, select_lists, env):
        pass
