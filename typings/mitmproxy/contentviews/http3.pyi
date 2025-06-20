"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterator
from dataclasses import dataclass
from . import base
from mitmproxy import flow, tcp

@dataclass(frozen=True)
class Frame:
    """Representation of an HTTP/3 frame."""
    type: int
    data: bytes
    def pretty(self): # -> list[Unknown]:
        ...
    


@dataclass(frozen=True)
class StreamType:
    """Representation of an HTTP/3 stream types."""
    type: int
    def pretty(self): # -> list[list[tuple[Literal['header'], str]]]:
        ...
    


@dataclass
class ConnectionState:
    message_count: int = ...
    frames: dict[int, list[Frame | StreamType]] = ...
    client_buf: bytearray = ...
    server_buf: bytearray = ...


class ViewHttp3(base.View):
    name = ...
    def __init__(self) -> None:
        ...
    
    def __call__(self, data, flow: flow.Flow | None = ..., tcp_message: tcp.TCPMessage | None = ..., **metadata): # -> tuple[Literal['HTTP/3'], list[Unknown]] | tuple[Literal['HTTP/3'], Iterator[TViewLine]]:
        ...
    
    def render_priority(self, data: bytes, flow: flow.Flow | None = ..., **metadata) -> float:
        ...
    


def fmt_frames(frames: list[Frame | StreamType]) -> Iterator[base.TViewLine]:
    ...

