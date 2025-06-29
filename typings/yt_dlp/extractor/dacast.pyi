"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class DacastBaseIE(InfoExtractor):
    _URL_TYPE = ...
    _API_INFO_URL = ...


class DacastVODIE(DacastBaseIE):
    _URL_TYPE = ...
    _TESTS = ...
    _WEBPAGE_TESTS = ...


class DacastPlaylistIE(DacastBaseIE):
    _URL_TYPE = ...
    _TESTS = ...
    _WEBPAGE_TESTS = ...


