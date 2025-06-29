"""
This type stub file was generated by pyright.
"""

import asyncio
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from mitmproxy import command
from mitmproxy.connection import Address
from mitmproxy.flow import Flow
from mitmproxy.proxy import events, mode_specs, server_hooks
from mitmproxy.proxy.mode_servers import ProxyConnectionHandler, ServerInstance, ServerManager

"""
This addon is responsible for starting/stopping the proxy server sockets/instances specified by the mode option.
"""
logger = ...
class Servers:
    def __init__(self, manager: ServerManager) -> None:
        ...
    
    @property
    def is_updating(self) -> bool:
        ...
    
    async def update(self, modes: Iterable[mode_specs.ProxyMode]) -> bool:
        ...
    
    def __len__(self) -> int:
        ...
    
    def __iter__(self) -> Iterator[ServerInstance]:
        ...
    
    def __getitem__(self, mode: str | mode_specs.ProxyMode) -> ServerInstance:
        ...
    


class Proxyserver(ServerManager):
    """
    This addon runs the actual proxy server.
    """
    connections: dict[tuple | str, ProxyConnectionHandler]
    servers: Servers
    is_running: bool
    _connect_addr: Address | None = ...
    _update_task: asyncio.Task | None = ...
    _inject_tasks: set[asyncio.Task]
    def __init__(self) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    @contextmanager
    def register_connection(self, connection_id: tuple | str, handler: ProxyConnectionHandler): # -> Generator[None, Any, None]:
        ...
    
    def load(self, loader): # -> None:
        ...
    
    def running(self): # -> None:
        ...
    
    def configure(self, updated) -> None:
        ...
    
    async def setup_servers(self) -> bool:
        """Setup proxy servers. This may take an indefinite amount of time to complete (e.g. on permission prompts)."""
        ...
    
    def listen_addrs(self) -> list[Address]:
        ...
    
    def inject_event(self, event: events.MessageInjected): # -> None:
        ...
    
    @command.command("inject.websocket")
    def inject_websocket(self, flow: Flow, to_client: bool, message: bytes, is_text: bool = ...): # -> None:
        ...
    
    @command.command("inject.tcp")
    def inject_tcp(self, flow: Flow, to_client: bool, message: bytes): # -> None:
        ...
    
    @command.command("inject.udp")
    def inject_udp(self, flow: Flow, to_client: bool, message: bytes): # -> None:
        ...
    
    def server_connect(self, data: server_hooks.ServerConnectionHookData): # -> None:
        ...
    


