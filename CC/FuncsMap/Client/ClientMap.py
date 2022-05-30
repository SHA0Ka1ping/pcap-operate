import sys
from CCDaemon import CCDaemon
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.Channel.MessageChannel import RecvState

from FuncsMap.Client.CommandFuncs import *

control_map = FuncsMap()
control_map.addCommand('Show', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: print(argv.split(maxsplit=1)[1]))
control_map.addCommand('End', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: sys.exit(0))
control_map.addCommand('Echo', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: echo(env, from_channel, select_lists, argv))
control_map.addCommand('RemoteExec', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: remoteExec(env, from_channel, select_lists, argv))
