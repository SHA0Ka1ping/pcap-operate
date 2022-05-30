from os import popen
import platform
import sys
from typing import Dict

from CCDaemon import CCDaemon
from SelectAction.Channel.ChannelDaemon import ChannelDaemon
from SelectAction.Channel.ChannelWriter import ChannelWriter
from SelectAction.Channel.MessageChannel import MessageChannel
from SelectAction.Channel.RouteManager import RouteManager
from SelectAction.base.SelectLists import SelectLists


def listConnection(env: CCDaemon):
    print([*env.control_Daemon.connect_list])


def echo(env: Dict[str, ChannelDaemon],
         from_channel: MessageChannel,
         select_lists: SelectLists,
         argv: str):
    # echo control_name message
    abbr, route_raw = argv.split(maxsplit=1)

    route_pack = RouteManager.unpackRoute(route_raw)
    route_id = route_pack['route_id']
    message = route_pack['message']

    channel_writer = ChannelWriter(
        from_channel, f'EchoRoute ' + RouteManager.packRoute(route_id, message))
    select_lists.outputs.append(channel_writer)


def remoteExec(env: Dict[str, ChannelDaemon],
               from_channel: MessageChannel,
               select_lists: SelectLists,
               argv: str):
    # echo control_name message
    abbr, route_raw = argv.split(maxsplit=1)

    route_pack = RouteManager.unpackRoute(route_raw)
    route_id = route_pack['route_id']
    command = route_pack['message']

    if platform.system() == 'Windows':
        command = 'powershell.exe ' + command
    command += ' 2>&1'

    print(command)

    with popen(command) as pipe:
        ret = pipe.read()

    channel_writer = ChannelWriter(
        from_channel, f'EchoRoute ' + RouteManager.packRoute(route_id, ret))
    select_lists.outputs.append(channel_writer)
