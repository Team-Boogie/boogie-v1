"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class RedBullTVIE(InfoExtractor):
    _VALID_URL = ...
    _TESTS = ...
    def extract_info(self, video_id): # -> dict[str, Unknown]:
        ...
    


class RedBullEmbedIE(RedBullTVIE):
    _VALID_URL = ...
    _TESTS = ...
    _VIDEO_ESSENSE_TMPL = ...


class RedBullTVRrnContentIE(InfoExtractor):
    _VALID_URL = ...
    _TESTS = ...


class RedBullIE(InfoExtractor):
    _VALID_URL = ...
    _TESTS = ...
    _INT_FALLBACK_LIST = ...
    _LAT_FALLBACK_MAP = ...


