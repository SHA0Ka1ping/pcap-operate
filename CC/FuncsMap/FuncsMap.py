from typing import Callable

from SelectAction.Channel.ChannelWriter import ChannelWriter
from SelectAction.base.ConnectionNotFound import ConnectionNotFound


class FuncsMap:
    def __init__(self) -> None:
        self.command_map = {}

    def addCommand(self, abbr: str, rstate: str, action: Callable):
        self.command_map[abbr] = {
            'rstate': rstate,  # At which state to run, abbr for 'run state'
            'action': action,
        }

    def _isReady(self, abbr: str, rstate: str):
        return self.command_map[abbr]['rstate'] == rstate

    def _getAction(self, abbr: str):
        return self.command_map[abbr]['action']

    def runCommand(self, abbr, rstate, env, from_channel, select_lists, argv):
        try:
            if self._isReady(abbr, rstate):
                self._getAction(abbr)(env, from_channel, select_lists, argv)
        except KeyError:
            channel_writer = ChannelWriter(
                from_channel, f'Show ' + 'CommandError: Command not found')
            select_lists.outputs.append(channel_writer)
        except ConnectionNotFound:
            channel_writer = ChannelWriter(
                from_channel, f'Show ' + 'ConnectionNotFound: No such connection')
            select_lists.outputs.append(channel_writer)
