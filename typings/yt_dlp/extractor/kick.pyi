"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class KickBaseIE(InfoExtractor):
    ...


class KickIE(KickBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
    


class KickVODIE(KickBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class KickClipIE(KickBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


