"""
This type stub file was generated by pyright.
"""

from typing import Union
from .exceptions import *
from .payloads import Payload

class BaseClient:
    def __init__(self, client_id: str, **kwargs) -> None:
        ...
    
    def update_event_loop(self, loop): # -> None:
        ...
    
    async def read_output(self): # -> Any:
        ...
    
    def send_data(self, op: int, payload: Union[dict, Payload]): # -> None:
        ...
    
    async def handshake(self): # -> None:
        ...
    


