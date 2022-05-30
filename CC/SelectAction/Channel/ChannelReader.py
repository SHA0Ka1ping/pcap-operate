import os
import sys
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.base.MessageAvailableAction import MessageAvailableAction
from SelectAction.Channel.MessageChannel import MessageChannel, RecvState
from SelectAction.base.SelectLists import SelectLists
from SelectAction.base.SocketAvailableAction import SocketAvailableAction


class ChannelReader(MessageAvailableAction):
    def __init__(self, message_channel: MessageChannel, command_map: FuncsMap) -> None:
        super().__init__(message_channel)
        self.command_map = command_map

    def __del__(self) -> None:
        # print('Closing Reader')
        self.socket.close()

    def availableAction(self, select_lists: SelectLists, env):
        state, segment_message, current_message = self.message_channel.read()
        # FIXME WIP. Some func can run under RECVING
        if state == RecvState.RECVALL:
            abbr = current_message.split(maxsplit=1)[0]
            self.command_map.runCommand(
                abbr, state, env, self.message_channel, select_lists, current_message)
