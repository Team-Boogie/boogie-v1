"""
This type stub file was generated by pyright.
"""

import collections
import enum
import time
import wsproto.handshake
from dataclasses import dataclass
from functools import cached_property
from logging import DEBUG, WARNING
from ...context import Context
from ...mode_specs import ReverseMode, UpstreamMode
from ..quic import QuicStreamEvent
from ._base import HttpCommand, HttpConnection, ReceiveHttp, StreamId
from ._events import HttpEvent, RequestData, RequestEndOfMessage, RequestHeaders, RequestProtocolError, RequestTrailers, ResponseData, ResponseEndOfMessage, ResponseHeaders, ResponseProtocolError, ResponseTrailers
from ._hooks import HttpConnectErrorHook, HttpConnectHook, HttpConnectedHook, HttpErrorHook, HttpRequestHeadersHook, HttpRequestHook, HttpResponseHeadersHook, HttpResponseHook
from ._http1 import Http1Client, Http1Connection, Http1Server
from ._http2 import Http2Client, Http2Server
from ._http3 import Http3Client, Http3Server
from mitmproxy import flow, http
from mitmproxy.connection import Connection, Server, TransportProtocol
from mitmproxy.net import server_spec
from mitmproxy.net.http import status_codes, url
from mitmproxy.net.http.http1 import expected_http_body_size
from mitmproxy.net.http.validate import validate_headers
from mitmproxy.proxy import commands, events, layer, tunnel
from mitmproxy.proxy.layers import quic, tcp, tls, websocket
from mitmproxy.proxy.layers.http import _upstream_proxy
from mitmproxy.proxy.utils import ReceiveBuffer, expect
from mitmproxy.utils import human
from mitmproxy.websocket import WebSocketData

class HTTPMode(enum.Enum):
    regular = ...
    transparent = ...
    upstream = ...


def validate_request(mode: HTTPMode, request: http.Request, validate_inbound_headers: bool) -> str | None:
    ...

def is_h3_alpn(alpn: bytes | None) -> bool:
    ...

@dataclass
class GetHttpConnection(HttpCommand):
    """
    Open an HTTP Connection. This may not actually open a connection, but return an existing HTTP connection instead.
    """
    blocking = ...
    address: tuple[str, int]
    tls: bool
    via: server_spec.ServerSpec | None
    transport_protocol: TransportProtocol = ...
    def __hash__(self) -> int:
        ...
    
    def connection_spec_matches(self, connection: Connection) -> bool:
        ...
    


@dataclass
class GetHttpConnectionCompleted(events.CommandCompleted):
    command: GetHttpConnection
    reply: tuple[None, str] | tuple[Connection, None]
    ...


@dataclass
class RegisterHttpConnection(HttpCommand):
    """
    Register that a HTTP connection attempt has been completed.
    """
    connection: Connection
    err: str | None
    ...


@dataclass
class SendHttp(HttpCommand):
    event: HttpEvent
    connection: Connection
    def __repr__(self) -> str:
        ...
    


@dataclass
class DropStream(HttpCommand):
    """Signal to the HTTP layer that this stream is done processing and can be dropped from memory."""
    stream_id: StreamId
    ...


class HttpStream(layer.Layer):
    request_body_buf: ReceiveBuffer
    response_body_buf: ReceiveBuffer
    flow: http.HTTPFlow
    stream_id: StreamId
    child_layer: layer.Layer | None = ...
    @cached_property
    def mode(self) -> HTTPMode:
        ...
    
    def __init__(self, context: Context, stream_id: int) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    @expect(RequestHeaders)
    def state_wait_for_request_headers(self, event: RequestHeaders) -> layer.CommandGenerator[None]:
        ...
    
    def start_request_stream(self) -> layer.CommandGenerator[None]:
        ...
    
    @expect(RequestData, RequestTrailers, RequestEndOfMessage)
    def state_stream_request_body(self, event: RequestData | RequestEndOfMessage) -> layer.CommandGenerator[None]:
        ...
    
    @expect(RequestData, RequestTrailers, RequestEndOfMessage)
    def state_consume_request_body(self, event: events.Event) -> layer.CommandGenerator[None]:
        ...
    
    @expect(ResponseHeaders)
    def state_wait_for_response_headers(self, event: ResponseHeaders) -> layer.CommandGenerator[None]:
        ...
    
    def start_response_stream(self) -> layer.CommandGenerator[None]:
        ...
    
    @expect(ResponseData, ResponseTrailers, ResponseEndOfMessage)
    def state_stream_response_body(self, event: events.Event) -> layer.CommandGenerator[None]:
        ...
    
    @expect(ResponseData, ResponseTrailers, ResponseEndOfMessage)
    def state_consume_response_body(self, event: events.Event) -> layer.CommandGenerator[None]:
        ...
    
    def send_response(self, already_streamed: bool = ...): # -> Generator[HttpResponseHook | Command | SendHttp, Unknown, None]:
        """We have either consumed the entire response from the server or the response was set by an addon."""
        ...
    
    def flow_done(self) -> layer.CommandGenerator[None]:
        ...
    
    def check_body_size(self, request: bool) -> layer.CommandGenerator[bool]:
        """
        Check if the body size exceeds limits imposed by stream_large_bodies or body_size_limit.

        Returns `True` if the body size exceeds body_size_limit and further processing should be stopped.
        """
        ...
    
    def check_invalid(self, request: bool) -> layer.CommandGenerator[bool]:
        ...
    
    def check_killed(self, emit_error_hook: bool) -> layer.CommandGenerator[bool]:
        ...
    
    def handle_protocol_error(self, event: RequestProtocolError | ResponseProtocolError) -> layer.CommandGenerator[None]:
        ...
    
    def make_server_connection(self) -> layer.CommandGenerator[bool]:
        ...
    
    def handle_connect(self) -> layer.CommandGenerator[None]:
        ...
    
    def handle_connect_regular(self): # -> Generator[OpenConnection | HttpConnectedHook | Command | HttpConnectErrorHook | SendHttp, Unknown, None]:
        ...
    
    def handle_connect_upstream(self): # -> Generator[HttpConnectedHook | Command | HttpConnectErrorHook | SendHttp, Unknown, None]:
        ...
    
    def handle_connect_finish(self): # -> Generator[HttpConnectedHook | Command | HttpConnectErrorHook | SendHttp, Unknown, None]:
        ...
    
    @expect(RequestData, RequestEndOfMessage, events.Event)
    def passthrough(self, event: events.Event) -> layer.CommandGenerator[None]:
        ...
    
    @expect()
    def state_uninitialized(self, _) -> layer.CommandGenerator[None]:
        ...
    
    @expect()
    def state_done(self, _) -> layer.CommandGenerator[None]:
        ...
    
    def state_errored(self, _) -> layer.CommandGenerator[None]:
        ...
    


class HttpLayer(layer.Layer):
    """
    ConnectionEvent: We have received b"GET /\r\n\r\n" from the client.
    HttpEvent: We have received request headers
    HttpCommand: Send request headers to X
    ConnectionCommand: Send b"GET /\r\n\r\n" to server.

    ConnectionEvent -> HttpEvent -> HttpCommand -> ConnectionCommand
    """
    mode: HTTPMode
    command_sources: dict[commands.Command, layer.Layer]
    streams: dict[int, HttpStream]
    connections: dict[Connection, layer.Layer]
    waiting_for_establishment: collections.defaultdict[Connection, list[GetHttpConnection]]
    def __init__(self, context: Context, mode: HTTPMode) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def event_to_child(self, child: layer.Layer | HttpStream, event: events.Event) -> layer.CommandGenerator[None]:
        ...
    
    def make_stream(self, stream_id: int) -> layer.CommandGenerator[None]:
        ...
    
    def get_connection(self, event: GetHttpConnection, *, reuse: bool = ...) -> layer.CommandGenerator[None]:
        ...
    
    def register_connection(self, command: RegisterHttpConnection) -> layer.CommandGenerator[None]:
        ...
    


class HttpClient(layer.Layer):
    child_layer: layer.Layer
    ...


