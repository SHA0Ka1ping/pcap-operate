from socket import socket
from SelectAction.Channel.ChannelReader import ChannelReader
from FuncsMap.FuncsMap import FuncsMap

from SelectAction.base.SelectLists import SelectLists
from SelectAction.Channel.ConnectedChannelMap import ConnectedChannelMap
from SelectAction.Channel.RouteManager import RouteManager
from SelectAction.Channel.MessageChannel import MessageChannel

from SelectAction.base.SocketAvailableAction import SocketAvailableAction
from SelectAction.base.KeyAgreement import keyAgreementServer


class ChannelDaemon(SocketAvailableAction):
    def __init__(self, daemon_socket: socket, command_map: FuncsMap) -> None:
        super().__init__(daemon_socket)
        self.command_map = command_map
        self.connected_channel_map = ConnectedChannelMap()
        self.route_map = RouteManager()

    def __del__(self) -> None:
        # print('Closing Daemon')
        self.socket.close()

    def availableAction(self, select_lists: SelectLists, env):
        channel_socket, addr = self.socket.accept()
        message_channel = MessageChannel(channel_socket, True)
        channel_reader = ChannelReader(
            message_channel, self.command_map)

        # print(channel_socket.getpeername()[0])
        self.connected_channel_map.addChannel(channel_socket, message_channel)
        select_lists.inputs.append(channel_reader)
