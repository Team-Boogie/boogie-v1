"""
This type stub file was generated by pyright.
"""

import contextlib
from typing import ClassVar, ContextManager
from setuptools.command.install import install as _install

"""Extends setuptools 'install' command."""
__all__ = ["Install"]
@contextlib.contextmanager
def suppress_known_deprecation() -> ContextManager:
    ...

class Install(_install):
    """Install everything from build directory."""
    command_name = ...
    user_options: ClassVar[list[tuple[str, str | None, str]]] = ...
    def expand_dirs(self) -> None:
        ...
    
    def get_sub_commands(self) -> list[str]:
        ...
    
    def initialize_options(self) -> None:
        ...
    
    def finalize_options(self) -> None:
        ...
    
    def select_scheme(self, name) -> None:
        ...
    
    def run(self) -> None:
        ...
    


