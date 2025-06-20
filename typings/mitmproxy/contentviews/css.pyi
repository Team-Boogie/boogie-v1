"""
This type stub file was generated by pyright.
"""

from mitmproxy.contentviews import base

CSS_SPECIAL_AREAS = ...
CSS_SPECIAL_CHARS = ...
def beautify(data: str, indent: str = ...): # -> str:
    """Beautify a string containing CSS code"""
    ...

class ViewCSS(base.View):
    name = ...
    def __call__(self, data, **metadata): # -> tuple[Literal['CSS'], Iterator[TViewLine]]:
        ...
    
    def render_priority(self, data: bytes, *, content_type: str | None = ..., **metadata) -> float:
        ...
    


if __name__ == "__main__":
    t = ...
    x = ...
