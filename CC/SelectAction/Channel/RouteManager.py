from hashlib import md5 as getHash
from time import time
from typing import Tuple

from SelectAction.Channel.MessageChannel import MessageChannel


class RouteManager():
    ROUTE_ID_LEN = 32

    def __init__(self) -> None:
        self.route_dict = {}

    def createRoute(self, command_channel: MessageChannel, control_channel: MessageChannel):
        route_id = getHash(
            f'{time()}'[2:].encode()
        ).hexdigest()[:RouteManager.ROUTE_ID_LEN]
        self.route_dict[route_id] = {
            'command_channel': command_channel,
            'control_channel': control_channel,
        }

        return route_id

    def popRoute(self, route_id):
        channel_pair = self.route_dict.pop(route_id)
        return channel_pair['command_channel'], channel_pair['control_channel']

    @staticmethod
    def packRoute(route_id, message):
        return route_id + message

    @staticmethod
    def unpackRoute(route_package: str):
        return {
            'route_id': route_package[:RouteManager.ROUTE_ID_LEN],
            'message': route_package[RouteManager.ROUTE_ID_LEN:],
        }
