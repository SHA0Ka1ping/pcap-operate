from select import select
from CCUtils import createUnblockedConnection
from SelectAction.Channel.ChannelReader import ChannelReader
from SelectAction.Channel.ChannelWriter import ChannelWriter
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.Channel.MessageChannel import MessageChannel, RecvState

from CCConfig import *
from SelectAction.base.SelectLists import SelectLists

from FuncsMap.Client.ClientMap import control_map


class CCClient:
    def __init__(self) -> None:
        self.message_channel = MessageChannel(
            createUnblockedConnection(DAEMON_HOST,
                                      CONTROL_PORT), False)
        control_reader = ChannelReader(self.message_channel, control_map)

        self.select_lists = SelectLists()
        self.select_lists.inputs.append(control_reader)

    def run(self) -> None:
        while True:
            # print(*self.select_lists) # DEBUG
            print('Check')
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
    cccmd = CCClient()
    cccmd.run()
