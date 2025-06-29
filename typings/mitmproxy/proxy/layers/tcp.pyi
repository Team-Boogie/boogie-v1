"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from mitmproxy import flow, tcp
from mitmproxy.proxy import events, layer
from mitmproxy.proxy.commands import StartHook
from mitmproxy.proxy.context import Context
from mitmproxy.proxy.events import MessageInjected
from mitmproxy.proxy.utils import expect

@dataclass
class TcpStartHook(StartHook):
    """
    A TCP connection has started.
    """
    flow: tcp.TCPFlow
    ...


@dataclass
class TcpMessageHook(StartHook):
    """
    A TCP connection has received a message. The most recent message
    will be flow.messages[-1]. The message is user-modifiable.
    """
    flow: tcp.TCPFlow
    ...


@dataclass
class TcpEndHook(StartHook):
    """
    A TCP connection has ended.
    """
    flow: tcp.TCPFlow
    ...


@dataclass
class TcpErrorHook(StartHook):
    """
    A TCP error has occurred.

    Every TCP flow will receive either a tcp_error or a tcp_end event, but not both.
    """
    flow: tcp.TCPFlow
    ...


class TcpMessageInjected(MessageInjected[tcp.TCPMessage]):
    """
    The user has injected a custom TCP message.
    """
    ...


class TCPLayer(layer.Layer):
    """
    Simple TCP layer that just relays messages right now.
    """
    flow: tcp.TCPFlow | None
    def __init__(self, context: Context, ignore: bool = ...) -> None:
        ...
    
    @expect(events.Start)
    def start(self, _) -> layer.CommandGenerator[None]:
        ...
    
    _handle_event = ...
    @expect(events.DataReceived, events.ConnectionClosed, TcpMessageInjected)
    def relay_messages(self, event: events.Event) -> layer.CommandGenerator[None]:
        ...
    
    @expect(events.DataReceived, events.ConnectionClosed, TcpMessageInjected)
    def done(self, _) -> layer.CommandGenerator[None]:
        ...
    


