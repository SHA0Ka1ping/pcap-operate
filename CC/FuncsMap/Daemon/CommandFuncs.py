from typing import Dict
from SelectAction.Channel.ChannelDaemon import ChannelDaemon
from SelectAction.Channel.ChannelWriter import ChannelWriter
from SelectAction.Channel.MessageChannel import MessageChannel
from SelectAction.Channel.RouteManager import RouteManager
from SelectAction.base.SelectLists import SelectLists


def listConnection(env: Dict[str, ChannelDaemon],
                   from_channel: MessageChannel,
                   select_lists: SelectLists,
                   argv: str):
    channel_writer = ChannelWriter(
        from_channel, f'Show ' + str([*(env['control_Daemon'].connected_channel_map)]))
    select_lists.outputs.append(channel_writer)


def echo(env: Dict[str, ChannelDaemon],
         from_channel: MessageChannel,
         select_lists: SelectLists,
         argv: str):
    # echo control_name message
    abbr, control_name, message = argv.split(maxsplit=2)
    message_channel = env['control_Daemon'].connected_channel_map.getChannel(
        control_name)
    route_id = env['control_Daemon'].route_map.createRoute(
        from_channel, message_channel)
    channel_writer = ChannelWriter(
        message_channel, f'Echo ' + RouteManager.packRoute(route_id, message))
    select_lists.outputs.append(channel_writer)


def echoRoute(env: Dict[str, ChannelDaemon],
              from_channel: MessageChannel,
              select_lists: SelectLists,
              argv: str):
    # echo control_name message
    abbr, route_raw = argv.split(maxsplit=1)

    route_pack = RouteManager.unpackRoute(route_raw)
    route_id = route_pack['route_id']
    message = route_pack['message']

    origin_channel, _ = env['control_Daemon'].route_map.popRoute(route_id)
    channel_writer = ChannelWriter(
        origin_channel, f'Show ' + message)
    select_lists.outputs.append(channel_writer)
    # print(message)


def remoteExec(env: Dict[str, ChannelDaemon],
               from_channel: MessageChannel,
               select_lists: SelectLists,
               argv: str):
    # echo control_name message
    abbr, control_name, command = argv.split(maxsplit=2)
    message_channel = env['control_Daemon'].connected_channel_map.getChannel(
        control_name)
    route_id = env['control_Daemon'].route_map.createRoute(
        from_channel, message_channel)
    channel_writer = ChannelWriter(
        message_channel, f'RemoteExec ' + RouteManager.packRoute(route_id, command))
    select_lists.outputs.append(channel_writer)
