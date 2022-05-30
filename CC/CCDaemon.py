import select
import sys

from CCConfig import *
from CCUtils import *
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.Channel.MessageChannel import RecvState
from SelectAction.Channel.RouteManager import RouteManager

from SelectAction.base.SelectLists import SelectLists
from SelectAction.Channel.ChannelDaemon import ChannelDaemon

from FuncsMap.Daemon.DaemonMap import command_map, control_map


class CCDaemon:
    def __init__(self) -> None:
        self.command_Daemon = ChannelDaemon(
            createUnblockedlistener(DAEMON_HOST,
                                    COMMAND_PORT),
            command_map,
        )
        self.control_Daemon = ChannelDaemon(
            createUnblockedlistener(DAEMON_HOST,
                                    CONTROL_PORT),
            control_map,
        )
        self.route_manager = RouteManager()

        self.select_lists = SelectLists()
        self.select_lists.inputs.append(self.command_Daemon)
        self.select_lists.inputs.append(self.control_Daemon)

    def run(self) -> None:
        while True:
            print('Check')
            # print(*self.select_lists)
            timeout = 1
            readable, writable, exceptional = select.select(
                *self.select_lists, timeout)

            for reader in readable:
                try:
                    self.select_lists.inputs.getAction(
                        reader).availableAction(
                            self.select_lists,
                            {
                                'command_Daemon': self.command_Daemon,
                                'control_Daemon': self.control_Daemon,
                                'route_manager': self.route_manager,
                            }
                    )
                except ConnectionError:  # Mostly due to close of socket
                    print('remove close reader')
                    self.select_lists.inputs.remove(reader)
                    self.control_Daemon.connected_channel_map.delChannel(
                        reader)
                    self.command_Daemon.connected_channel_map.delChannel(
                        reader)

            for writer in writable:
                self.select_lists.outputs.getAction(
                    writer).availableAction(self.select_lists, None)
            for exception in exceptional:
                print('exception')


if __name__ == '__main__':
    ccDaemon = CCDaemon()
    ccDaemon.run()
