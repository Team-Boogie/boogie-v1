"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class GlomexBaseIE(InfoExtractor):
    _DEFAULT_ORIGIN_URL = ...
    _API_URL = ...


class GlomexIE(GlomexBaseIE):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _INTEGRATION_ID = ...
    _TESTS = ...


class GlomexEmbedIE(GlomexBaseIE):
    IE_NAME = ...
    IE_DESC = ...
    _BASE_PLAYER_URL = ...
    _BASE_PLAYER_URL_RE = ...
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def build_player_url(cls, video_id, integration, origin_url=...):
        ...
    


