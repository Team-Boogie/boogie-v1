"""
This type stub file was generated by pyright.
"""

import enum
import functools
from .common import InfoExtractor, SearchInfoExtractor
from ..utils import classproperty

STREAMING_DATA_CLIENT_NAME = ...
STREAMING_DATA_PO_TOKEN = ...
INNERTUBE_CLIENTS = ...
def short_client_name(client_name): # -> str:
    ...

def build_innertube_clients(): # -> None:
    ...

class BadgeType(enum.Enum):
    AVAILABILITY_UNLISTED = ...
    AVAILABILITY_PRIVATE = ...
    AVAILABILITY_PUBLIC = ...
    AVAILABILITY_PREMIUM = ...
    AVAILABILITY_SUBSCRIPTION = ...
    LIVE_NOW = ...
    VERIFIED = ...


class YoutubeBaseInfoExtractor(InfoExtractor):
    """Provide base functions for Youtube extractors"""
    _RESERVED_NAMES = ...
    _PLAYLIST_ID_RE = ...
    _LOGIN_REQUIRED = ...
    _INVIDIOUS_SITES = ...
    _SUPPORTED_LANG_CODES = ...
    _IGNORED_WARNINGS = ...
    _YT_HANDLE_RE = ...
    _YT_CHANNEL_UCID_RE = ...
    _NETRC_MACHINE = ...
    def ucid_or_none(self, ucid): # -> str | Any | tuple[str | Unknown, ...] | type[NO_DEFAULT] | None:
        ...
    
    def handle_or_none(self, handle): # -> str | Any | tuple[str | Unknown, ...] | type[NO_DEFAULT] | None:
        ...
    
    def handle_from_url(self, url): # -> str | Any | tuple[str | Unknown, ...] | type[NO_DEFAULT] | None:
        ...
    
    def ucid_from_url(self, url): # -> str | Any | tuple[str | Unknown, ...] | type[NO_DEFAULT] | None:
        ...
    
    _YT_INITIAL_DATA_RE = ...
    _YT_INITIAL_PLAYER_RESPONSE_RE = ...
    _SAPISID = ...
    def extract_yt_initial_data(self, item_id, webpage, fatal=...): # -> type[NO_DEFAULT] | dict[Unknown, Unknown] | Any | None:
        ...
    
    @functools.cached_property
    def is_authenticated(self): # -> bool:
        ...
    
    def extract_ytcfg(self, video_id, webpage): # -> dict[Unknown, Unknown] | Any | dict[Any, Any]:
        ...
    
    def generate_api_headers(self, *, ytcfg=..., account_syncid=..., session_index=..., visitor_data=..., api_hostname=..., default_client=..., **kwargs): # -> dict[str | Unknown, Unknown]:
        ...
    
    @staticmethod
    def extract_relative_time(relative_time_text): # -> datetime | None:
        """
        Extracts a relative time from string and converts to dt object
        e.g. 'streamed 6 days ago', '5 seconds ago (edited)', 'updated today', '8 yr ago'
        """
        ...
    
    @staticmethod
    def is_music_url(url): # -> bool:
        ...
    


class YoutubeIE(YoutubeBaseInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    _EMBED_REGEX = ...
    _RETURN_TYPE = ...
    _PLAYER_INFO_RE = ...
    _formats = ...
    _SUBTITLE_FORMATS = ...
    _DEFAULT_CLIENTS = ...
    _DEFAULT_AUTHED_CLIENTS = ...
    _GEO_BYPASS = ...
    IE_NAME = ...
    _TESTS = ...
    _WEBPAGE_TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
    
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    @classmethod
    def extract_id(cls, url):
        ...
    
    def fetch_po_token(self, client=..., visitor_data=..., data_sync_id=..., player_url=..., **kwargs): # -> None:
        ...
    


class YoutubeTabBaseInfoExtractor(YoutubeBaseInfoExtractor):
    @staticmethod
    def passthrough_smuggled_data(func): # -> _Wrapped[..., Unknown, (self: Unknown, url: Unknown), Unknown]:
        ...
    
    @functools.cached_property
    def skip_webpage(self):
        ...
    
    _SEARCH_PARAMS = ...


class YoutubeTabIE(YoutubeTabBaseInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    IE_NAME = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
    
    _URL_RE = ...


class YoutubePlaylistIE(YoutubeBaseInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    IE_NAME = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
    


class YoutubeYtBeIE(YoutubeBaseInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeLivestreamEmbedIE(YoutubeBaseInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeYtUserIE(YoutubeBaseInfoExtractor):
    IE_DESC = ...
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeFavouritesIE(YoutubeBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _LOGIN_REQUIRED = ...
    _TESTS = ...


class YoutubeNotificationsIE(YoutubeTabBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _LOGIN_REQUIRED = ...
    _TESTS = ...


class YoutubeSearchIE(YoutubeTabBaseInfoExtractor, SearchInfoExtractor):
    IE_DESC = ...
    IE_NAME = ...
    _SEARCH_KEY = ...
    _SEARCH_PARAMS = ...
    _TESTS = ...


class YoutubeSearchDateIE(YoutubeTabBaseInfoExtractor, SearchInfoExtractor):
    IE_NAME = ...
    _SEARCH_KEY = ...
    IE_DESC = ...
    _SEARCH_PARAMS = ...
    _TESTS = ...


class YoutubeSearchURLIE(YoutubeTabBaseInfoExtractor):
    IE_DESC = ...
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeMusicSearchURLIE(YoutubeTabBaseInfoExtractor):
    IE_DESC = ...
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _SECTIONS = ...


class YoutubeFeedsInfoExtractor(YoutubeBaseInfoExtractor):
    """
    Base class for feed extractors
    Subclasses must re-define the _FEED_NAME property.
    """
    _LOGIN_REQUIRED = ...
    _FEED_NAME = ...
    @classproperty
    def IE_NAME(cls): # -> LiteralString:
        ...
    


class YoutubeWatchLaterIE(YoutubeBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeRecommendedIE(YoutubeFeedsInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    _FEED_NAME = ...
    _LOGIN_REQUIRED = ...
    _TESTS = ...


class YoutubeSubscriptionsIE(YoutubeFeedsInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    _FEED_NAME = ...
    _TESTS = ...


class YoutubeHistoryIE(YoutubeFeedsInfoExtractor):
    IE_DESC = ...
    _VALID_URL = ...
    _FEED_NAME = ...
    _TESTS = ...


class YoutubeShortsAudioPivotIE(YoutubeBaseInfoExtractor):
    IE_DESC = ...
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeTruncatedURLIE(YoutubeBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeClipIE(YoutubeTabBaseInfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeConsentRedirectIE(YoutubeBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class YoutubeTruncatedIDIE(YoutubeBaseInfoExtractor):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


