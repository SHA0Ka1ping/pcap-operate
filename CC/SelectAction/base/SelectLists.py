from socket import socket

from numpy import isin
from SelectAction.base.SocketAvailableAction import SocketAvailableAction


class SelectLists:
    def __init__(self) -> None:
        class SocketList:
            def __init__(self) -> None:
                self.socket_dict = {}

            def __iter__(self):
                return iter([list(self.socket_dict.keys())])

            def getAction(self, socket: socket) -> SocketAvailableAction:
                return self.socket_dict[socket]

            def append(self, action: SocketAvailableAction):
                self.socket_dict[action.socket] = action

            def remove(self, _o: object):
                if isinstance(_o, SocketAvailableAction):
                    self.socket_dict.pop(_o.socket)
                elif isinstance(_o, socket):
                    self.socket_dict.pop(_o)

            def isEmpty(self):
                return self.socket_dict == {}
        self.inputs = SocketList()
        self.outputs = SocketList()
        self.exceptions = self.inputs

    def __iter__(self):
        return iter([*self.inputs,
                     *self.outputs,
                     *self.exceptions])

    def isEmpty(self):
        return self.inputs.isEmpty() \
            and self.outputs.isEmpty() \
            and self.exceptions.isEmpty()


if __name__ == '__main__':
    print(*SelectLists())
