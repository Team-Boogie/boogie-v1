"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from wsproto.frame_protocol import Opcode
from mitmproxy.coretypes import serializable

"""
Mitmproxy used to have its own WebSocketFlow type until mitmproxy 6, but now WebSocket connections now are represented
as HTTP flows as well. They can be distinguished from regular HTTP requests by having the
`mitmproxy.http.HTTPFlow.websocket` attribute set.

This module only defines the classes for individual `WebSocketMessage`s and the `WebSocketData` container.
"""
WebSocketMessageState = tuple[int, bool, bytes, float, bool, bool]
class WebSocketMessage(serializable.Serializable):
    """
    A single WebSocket message sent from one peer to the other.

    Fragmented WebSocket messages are reassembled by mitmproxy and then
    represented as a single instance of this class.

    The [WebSocket RFC](https://tools.ietf.org/html/rfc6455) specifies both
    text and binary messages. To avoid a whole class of nasty type confusion bugs,
    mitmproxy stores all message contents as `bytes`. If you need a `str`, you can access the `text` property
    on text messages:

    >>> if message.is_text:
    >>>     text = message.text
    """
    from_client: bool
    type: Opcode
    content: bytes
    timestamp: float
    dropped: bool
    injected: bool
    def __init__(self, type: int | Opcode, from_client: bool, content: bytes, timestamp: float | None = ..., dropped: bool = ..., injected: bool = ...) -> None:
        ...
    
    @classmethod
    def from_state(cls, state: WebSocketMessageState): # -> Self@WebSocketMessage:
        ...
    
    def get_state(self) -> WebSocketMessageState:
        ...
    
    def set_state(self, state: WebSocketMessageState) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    @property
    def is_text(self) -> bool:
        """
        `True` if this message is assembled from WebSocket `TEXT` frames,
        `False` if it is assembled from `BINARY` frames.
        """
        ...
    
    def drop(self): # -> None:
        """Drop this message, i.e. don't forward it to the other peer."""
        ...
    
    def kill(self): # -> None:
        """A deprecated alias for `.drop()`."""
        ...
    
    @property
    def text(self) -> str:
        """
        The message content as text.

        This attribute is only available if `WebSocketMessage.is_text` is `True`.

        *See also:* `WebSocketMessage.content`
        """
        ...
    
    @text.setter
    def text(self, value: str) -> None:
        ...
    


@dataclass
class WebSocketData(serializable.SerializableDataclass):
    """
    A data container for everything related to a single WebSocket connection.
    This is typically accessed as `mitmproxy.http.HTTPFlow.websocket`.
    """
    messages: list[WebSocketMessage] = ...
    closed_by_client: bool | None = ...
    close_code: int | None = ...
    close_reason: str | None = ...
    timestamp_end: float | None = ...
    def __repr__(self): # -> str:
        ...
    


