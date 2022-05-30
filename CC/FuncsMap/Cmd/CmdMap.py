import sys

from sympy import arg
from CCDaemon import CCDaemon
from FuncsMap.FuncsMap import FuncsMap
from SelectAction.Channel.MessageChannel import RecvState

from FuncsMap.Cmd.CommandFuncs import *

command_map = FuncsMap()
command_map.addCommand('Show', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: show(argv))
command_map.addCommand('End', RecvState.RECVALL,
                       lambda env, from_channel, select_lists, argv: sys.exit(0))
