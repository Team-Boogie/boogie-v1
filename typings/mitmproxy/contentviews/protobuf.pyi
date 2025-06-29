"""
This type stub file was generated by pyright.
"""

from . import base

def write_buf(out, field_tag, body, indent_level): # -> None:
    ...

def format_pbuf(raw): # -> str | Literal[False]:
    ...

class ViewProtobuf(base.View):
    """Human friendly view of protocol buffers
    The view uses the protoc compiler to decode the binary
    """
    name = ...
    __content_types = ...
    def __call__(self, data, **metadata): # -> tuple[Literal['Protobuf'], Iterator[TViewLine]]:
        ...
    
    def render_priority(self, data: bytes, *, content_type: str | None = ..., **metadata) -> float:
        ...
    


