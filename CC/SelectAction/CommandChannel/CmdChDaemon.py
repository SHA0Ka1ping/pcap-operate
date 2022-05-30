import socket

from SelectAction.base.SocketAvailableAction import SocketAvailableAction
from SelectAction.base.KeyAgreement import keyAgreementServer


# Command Channel Daemon
class CmdChDaemon(SocketAvailableAction):
    def availableAction(self, select_lists):
        channel_socket, addr = self.socket.accept()
        pipeIN, pipeOUT = keyAgreementServer(channel_socket)
