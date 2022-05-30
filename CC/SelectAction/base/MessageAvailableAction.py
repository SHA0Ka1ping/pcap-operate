from socket import socket
from abc import ABC, abstractclassmethod

from SelectAction.base.SocketAvailableAction import SocketAvailableAction
from SelectAction.Channel.MessageChannel import MessageChannel


class MessageAvailableAction(SocketAvailableAction):
    def __init__(self, message_channel: MessageChannel) -> None:
        super().__init__(message_channel.socket)
        self.message_channel = message_channel
