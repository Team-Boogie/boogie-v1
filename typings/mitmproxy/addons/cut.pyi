"""
This type stub file was generated by pyright.
"""

import mitmproxy.types
from collections.abc import Sequence
from mitmproxy import command, flow

logger = ...
def headername(spec: str): # -> str:
    ...

def is_addr(v): # -> bool:
    ...

def extract(cut: str, f: flow.Flow) -> str | bytes:
    ...

def extract_str(cut: str, f: flow.Flow) -> str:
    ...

class Cut:
    @command.command("cut")
    def cut(self, flows: Sequence[flow.Flow], cuts: mitmproxy.types.CutSpec) -> mitmproxy.types.Data:
        """
        Cut data from a set of flows. Cut specifications are attribute paths
        from the base of the flow object, with a few conveniences - "port"
        and "host" retrieve parts of an address tuple, ".header[key]"
        retrieves a header value. Return values converted to strings or
        bytes: SSL certificates are converted to PEM format, bools are "true"
        or "false", "bytes" are preserved, and all other values are
        converted to strings.
        """
        ...
    
    @command.command("cut.save")
    def save(self, flows: Sequence[flow.Flow], cuts: mitmproxy.types.CutSpec, path: mitmproxy.types.Path) -> None:
        """
        Save cuts to file. If there are multiple flows or cuts, the format
        is UTF-8 encoded CSV. If there is exactly one row and one column,
        the data is written to file as-is, with raw bytes preserved. If the
        path is prefixed with a "+", values are appended if there is an
        existing file.
        """
        ...
    
    @command.command("cut.clip")
    def clip(self, flows: Sequence[flow.Flow], cuts: mitmproxy.types.CutSpec) -> None:
        """
        Send cuts to the clipboard. If there are multiple flows or cuts, the
        format is UTF-8 encoded CSV. If there is exactly one row and one
        column, the data is written to file as-is, with raw bytes preserved.
        """
        ...
    


