"""
This type stub file was generated by pyright.
"""

from mitmproxy import http

TOrigin = tuple[str, int, str]
def ckey(attrs: dict[str, str], f: http.HTTPFlow) -> TOrigin:
    """
    Returns a (domain, port, path) tuple.
    """
    ...

def domain_match(a: str, b: str) -> bool:
    ...

class StickyCookie:
    def __init__(self) -> None:
        ...
    
    def load(self, loader): # -> None:
        ...
    
    def configure(self, updated): # -> None:
        ...
    
    def response(self, flow: http.HTTPFlow): # -> None:
        ...
    
    def request(self, flow: http.HTTPFlow): # -> None:
        ...
    


