import os
import sys
from SelectAction.base.MessageAvailableAction import MessageAvailableAction
from SelectAction.Channel.MessageChannel import MessageChannel, SendState
from SelectAction.base.SelectLists import SelectLists
from SelectAction.base.SocketAvailableAction import SocketAvailableAction


class ChannelWriter(MessageAvailableAction):
    def __init__(self, message_channel: MessageChannel, message: str) -> None:
        super().__init__(message_channel)
        self.message_send_task = message_channel.send(message)()

    def availableAction(self, select_lists: SelectLists, env):
        state, send_cnt = next(self.message_send_task)
        # print(state == SendState.SENDALL)
        if state == SendState.SENDALL:
            select_lists.outputs.remove(self)
