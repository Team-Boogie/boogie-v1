"""
This type stub file was generated by pyright.
"""

from . import base

class ViewRaw(base.View):
    name = ...
    def __call__(self, data, **metadata): # -> tuple[Literal['Raw'], Iterator[TViewLine]]:
        ...
    
    def render_priority(self, data: bytes, **metadata) -> float:
        ...
    


