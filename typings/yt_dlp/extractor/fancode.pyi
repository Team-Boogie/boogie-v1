"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class FancodeVodIE(InfoExtractor):
    _WORKING = ...
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _ACCESS_TOKEN = ...
    _NETRC_MACHINE = ...
    _LOGIN_HINT = ...
    headers = ...
    def download_gql(self, variable, data, note, fatal=..., headers=...): # -> Any | Literal[False]:
        ...
    


class FancodeLiveIE(FancodeVodIE):
    _WORKING = ...
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


