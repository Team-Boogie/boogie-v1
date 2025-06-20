"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class DailymotionBaseInfoExtractor(InfoExtractor):
    _FAMILY_FILTER = ...
    _HEADERS = ...
    _NETRC_MACHINE = ...


class DailymotionIE(DailymotionBaseInfoExtractor):
    _VALID_URL = ...
    IE_NAME = ...
    _EMBED_REGEX = ...
    _TESTS = ...
    _WEBPAGE_TESTS = ...
    _GEO_BYPASS = ...
    _COMMON_MEDIA_FIELDS = ...


class DailymotionPlaylistBaseIE(DailymotionBaseInfoExtractor):
    _PAGE_SIZE = ...


class DailymotionPlaylistIE(DailymotionPlaylistBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _OBJECT_TYPE = ...


class DailymotionSearchIE(DailymotionPlaylistBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _PAGE_SIZE = ...
    _TESTS = ...
    _SEARCH_QUERY = ...


class DailymotionUserIE(DailymotionPlaylistBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _OBJECT_TYPE = ...


