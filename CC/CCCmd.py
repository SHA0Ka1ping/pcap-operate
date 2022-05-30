import sys
from socket import socket
from select import select
from CCUtils import createUnblockedConnection
from SelectAction.Channel.ChannelReader import ChannelReader
from SelectAction.Channel.ChannelWriter import ChannelWriter
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.Channel.MessageChannel import MessageChannel, RecvState

from CCConfig import *
from SelectAction.base.SelectLists import SelectLists

from FuncsMap.Cmd.CmdMap import command_map


class CCCmd:
    def __init__(self, command='Show asdasdasdasd') -> None:
        message_channel = MessageChannel(
            createUnblockedConnection(DAEMON_HOST,
                                      COMMAND_PORT), False)
        command_reader = ChannelReader(message_channel, command_map)
        command_writer = ChannelWriter(message_channel, command)

        self.select_lists = SelectLists()
        self.select_lists.inputs.append(command_reader)
        self.select_lists.outputs.append(command_writer)

    def run(self) -> None:
        while True:
            # print(*self.select_lists)
            # print('Check')
            timeout = 1
            readable, writable, exceptional = select(
                *self.select_lists, timeout)

            for reader in readable:
                # print('reader')
                try:
                    self.select_lists.inputs.getAction(
                        reader).availableAction(self.select_lists, None)
                except ConnectionError:  # Mostly due to close of socket
                    self.select_lists.inputs.remove(reader)

            for writer in writable:
                # print('writer')
                self.select_lists.outputs.getAction(
                    writer).availableAction(self.select_lists, None)
            for exception in exceptional:
                print('exception')


if __name__ == '__main__':
    cccmd = CCCmd(' '.join(sys.argv[1:]))
    # cccmd = CCCmd()
    cccmd.run()
