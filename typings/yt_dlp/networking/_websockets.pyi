"""
This type stub file was generated by pyright.
"""

import websockets.sync.client
from .common import register_rh
from .websocket import WebSocketRequestHandler, WebSocketResponse
from ..dependencies import websockets

if not websockets:
    ...
websockets_version = ...
if websockets_version < (13, 0):
    ...
class WebsocketsResponseAdapter(WebSocketResponse):
    def __init__(self, ws: websockets.sync.client.ClientConnection, url) -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    def send(self, message):
        ...
    
    def recv(self):
        ...
    


@register_rh
class WebsocketsRH(WebSocketRequestHandler):
    """
    Websockets request handler
    https://websockets.readthedocs.io
    https://github.com/python-websockets/websockets
    """
    _SUPPORTED_URL_SCHEMES = ...
    _SUPPORTED_PROXY_SCHEMES = ...
    _SUPPORTED_FEATURES = ...
    RH_NAME = ...
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def close(self): # -> None:
        ...
    


