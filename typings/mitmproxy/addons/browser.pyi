"""
This type stub file was generated by pyright.
"""

import subprocess
import tempfile
from mitmproxy import command

def find_executable_cmd(*search_paths) -> list[str] | None:
    ...

def find_flatpak_cmd(*search_paths) -> list[str] | None:
    ...

class Browser:
    browser: list[subprocess.Popen] = ...
    tdir: list[tempfile.TemporaryDirectory] = ...
    @command.command("browser.start")
    def start(self, browser: str = ...) -> None:
        ...
    
    def launch_chrome(self) -> None:
        """
        Start an isolated instance of Chrome that points to the currently
        running proxy.
        """
        ...
    
    def launch_firefox(self) -> None:
        """
        Start an isolated instance of Firefox that points to the currently
        running proxy.
        """
        ...
    
    def done(self): # -> None:
        ...
    


