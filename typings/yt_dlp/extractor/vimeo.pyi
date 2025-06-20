"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class VimeoBaseInfoExtractor(InfoExtractor):
    _NETRC_MACHINE = ...
    _LOGIN_REQUIRED = ...
    _LOGIN_URL = ...


class VimeoIE(VimeoBaseInfoExtractor):
    """Information extractor for vimeo.com."""
    _VALID_URL = ...
    IE_NAME = ...
    _EMBED_REGEX = ...
    _TESTS = ...


class VimeoOndemandIE(VimeoIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class VimeoChannelIE(VimeoBaseInfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _MORE_PAGES_INDICATOR = ...
    _TITLE = ...
    _TITLE_RE = ...
    _TESTS = ...
    _BASE_URL_TEMPL = ...


class VimeoUserIE(VimeoChannelIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TITLE_RE = ...
    _TESTS = ...
    _BASE_URL_TEMPL = ...


class VimeoAlbumIE(VimeoBaseInfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _TITLE_RE = ...
    _TESTS = ...
    _PAGE_SIZE = ...


class VimeoGroupsIE(VimeoChannelIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _BASE_URL_TEMPL = ...


class VimeoReviewIE(VimeoBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class VimeoWatchLaterIE(VimeoChannelIE):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TITLE = ...
    _LOGIN_REQUIRED = ...
    _TESTS = ...


class VimeoLikesIE(VimeoChannelIE):
    _VALID_URL = ...
    IE_NAME = ...
    IE_DESC = ...
    _TESTS = ...


class VHXEmbedIE(VimeoBaseInfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _EMBED_REGEX = ...


class VimeoProIE(VimeoBaseInfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


