"""
This type stub file was generated by pyright.
"""

import mitmproxy.hooks
import mitmproxy.proxy.layer
from typing import TYPE_CHECKING, Union
from mitmproxy.connection import Connection, Server

"""
Commands make it possible for layers to communicate with the "outer world",
e.g. to perform IO or to ask the master.
A command is issued by a proxy layer and is then passed upwards to the proxy server, and from there
possibly to the master and addons.

The counterpart to commands are events.
"""
if TYPE_CHECKING:
    ...
class Command:
    """
    Base class for all commands
    """
    blocking: Union[bool, mitmproxy.proxy.layer.Layer] = ...
    def __repr__(self): # -> str:
        ...
    


class RequestWakeup(Command):
    """
    Request a `Wakeup` event after the specified amount of seconds.
    """
    delay: float
    def __init__(self, delay: float) -> None:
        ...
    


class ConnectionCommand(Command):
    """
    Commands involving a specific connection
    """
    connection: Connection
    def __init__(self, connection: Connection) -> None:
        ...
    


class SendData(ConnectionCommand):
    """
    Send data to a remote peer
    """
    data: bytes
    def __init__(self, connection: Connection, data: bytes) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    


class OpenConnection(ConnectionCommand):
    """
    Open a new connection
    """
    connection: Server
    blocking = ...


class CloseConnection(ConnectionCommand):
    """
    Close a connection. If the client connection is closed,
    all other connections will ultimately be closed during cleanup.
    """
    ...


class CloseTcpConnection(CloseConnection):
    half_close: bool
    def __init__(self, connection: Connection, half_close: bool = ...) -> None:
        ...
    


class StartHook(Command, mitmproxy.hooks.Hook):
    """
    Start an event hook in the mitmproxy core.
    This triggers a particular function (derived from the class name) in all addons.
    """
    name = ...
    blocking = ...
    def __new__(cls, *args, **kwargs): # -> Self@StartHook:
        ...
    


class Log(Command):
    """
    Log a message.

    Layers could technically call `logging.log` directly, but the use of a command allows us to
    write more expressive playbook tests. Put differently, by using commands we can assert that
    a specific log message is a direct consequence of a particular I/O event.
    This could also be implemented with some more playbook magic in the future,
    but for now we keep the current approach as the fully sans-io one.
    """
    message: str
    level: int
    def __init__(self, message: str, level: int = ...) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    


