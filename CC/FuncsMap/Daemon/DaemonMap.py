import sys
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.Channel.MessageChannel import RecvState

from FuncsMap.Daemon.CommandFuncs import *

command_map = FuncsMap()
command_map.addCommand('ListConnection', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: listConnection(env, from_channel, select_lists, argv))
command_map.addCommand('Echo', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: echo(env, from_channel, select_lists, argv))
command_map.addCommand('RemoteExec', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: remoteExec(env, from_channel, select_lists, argv))
command_map.addCommand('Show', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: print(argv.split(maxsplit=1)[1]))
command_map.addCommand('End', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: sys.exit(0))

control_map = FuncsMap()
control_map.addCommand('Show', RecvState.RECVALL,
                       lambda message: print(message))
control_map.addCommand('End', RecvState.RECVALL,
                       lambda: sys.exit(0))
control_map.addCommand('EchoRoute', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: echoRoute(env, from_channel, select_lists, argv))
