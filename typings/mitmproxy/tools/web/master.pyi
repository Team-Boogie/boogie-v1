"""
This type stub file was generated by pyright.
"""

from mitmproxy import master, options

logger = ...
class WebMaster(master.Master):
    def __init__(self, opts: options.Options, with_termlog: bool = ...) -> None:
        ...
    
    async def running(self): # -> None:
        ...
    


