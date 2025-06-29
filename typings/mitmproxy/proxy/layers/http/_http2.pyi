"""
This type stub file was generated by pyright.
"""

import collections
import h2.config
import h2.events
from collections.abc import Sequence
from enum import Enum
from typing import ClassVar
from ...context import Context
from ...events import ConnectionClosed, DataReceived, Event, Wakeup
from ...layer import CommandGenerator
from ...utils import expect
from . import RequestData, RequestEndOfMessage, RequestHeaders, RequestProtocolError, RequestTrailers, ResponseData, ResponseEndOfMessage, ResponseHeaders, ResponseProtocolError, ResponseTrailers
from ._base import HttpConnection, HttpEvent
from ._http_h2 import BufferedH2Connection
from mitmproxy import http
from mitmproxy.connection import Connection

class StreamState(Enum):
    EXPECTING_HEADERS = ...
    HEADERS_RECEIVED = ...


CATCH_HYPER_H2_ERRORS = ...
class Http2Connection(HttpConnection):
    h2_conf: ClassVar[h2.config.H2Configuration]
    h2_conf_defaults = ...
    h2_conn: BufferedH2Connection
    streams: dict[int, StreamState]
    ReceiveProtocolError: type[RequestProtocolError | ResponseProtocolError]
    ReceiveData: type[RequestData | ResponseData]
    ReceiveTrailers: type[RequestTrailers | ResponseTrailers]
    ReceiveEndOfMessage: type[RequestEndOfMessage | ResponseEndOfMessage]
    def __init__(self, context: Context, conn: Connection) -> None:
        ...
    
    def is_closed(self, stream_id: int) -> bool:
        """Check if a non-idle stream is closed"""
        ...
    
    def is_open_for_us(self, stream_id: int) -> bool:
        """Check if we can write to a non-idle stream."""
        ...
    
    def handle_h2_event(self, event: h2.events.Event) -> CommandGenerator[bool]:
        """returns true if further processing should be stopped."""
        ...
    
    def protocol_error(self, message: str, error_code: int = ...) -> CommandGenerator[None]:
        ...
    
    def close_connection(self, msg: str) -> CommandGenerator[None]:
        ...
    
    @expect(DataReceived, HttpEvent, ConnectionClosed, Wakeup)
    def done(self, _) -> CommandGenerator[None]:
        ...
    


def normalize_h1_headers(headers: list[tuple[bytes, bytes]], is_client: bool) -> list[tuple[bytes, bytes]]:
    ...

def normalize_h2_headers(headers: list[tuple[bytes, bytes]]) -> CommandGenerator[None]:
    ...

def format_h2_request_headers(context: Context, event: RequestHeaders) -> CommandGenerator[list[tuple[bytes, bytes]]]:
    ...

def format_h2_response_headers(context: Context, event: ResponseHeaders) -> CommandGenerator[list[tuple[bytes, bytes]]]:
    ...

class Http2Server(Http2Connection):
    h2_conf = ...
    ReceiveProtocolError = RequestProtocolError
    ReceiveData = RequestData
    ReceiveTrailers = RequestTrailers
    ReceiveEndOfMessage = RequestEndOfMessage
    def __init__(self, context: Context) -> None:
        ...
    
    def handle_h2_event(self, event: h2.events.Event) -> CommandGenerator[bool]:
        ...
    


class Http2Client(Http2Connection):
    h2_conf = ...
    ReceiveProtocolError = ResponseProtocolError
    ReceiveData = ResponseData
    ReceiveTrailers = ResponseTrailers
    ReceiveEndOfMessage = ResponseEndOfMessage
    our_stream_id: dict[int, int]
    their_stream_id: dict[int, int]
    stream_queue: collections.defaultdict[int, list[Event]]
    provisional_max_concurrency: int | None = ...
    last_activity: float
    def __init__(self, context: Context) -> None:
        ...
    
    def handle_h2_event(self, event: h2.events.Event) -> CommandGenerator[bool]:
        ...
    


def split_pseudo_headers(h2_headers: Sequence[tuple[bytes, bytes]]) -> tuple[dict[bytes, bytes], http.Headers]:
    ...

def parse_h2_request_headers(h2_headers: Sequence[tuple[bytes, bytes]]) -> tuple[str, int, bytes, bytes, bytes, bytes, http.Headers]:
    """Split HTTP/2 pseudo-headers from the actual headers and parse them."""
    ...

def parse_h2_response_headers(h2_headers: Sequence[tuple[bytes, bytes]]) -> tuple[int, http.Headers]:
    """Split HTTP/2 pseudo-headers from the actual headers and parse them."""
    ...

__all__ = ["format_h2_request_headers", "format_h2_response_headers", "parse_h2_request_headers", "parse_h2_response_headers", "Http2Client", "Http2Server"]
