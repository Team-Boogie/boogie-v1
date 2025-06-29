"""
This type stub file was generated by pyright.
"""

import functools
from .common import InfoExtractor

class PatreonBaseIE(InfoExtractor):
    @functools.cached_property
    def patreon_user_agent(self): # -> Literal['Patreon/72.2.28 (Android; Android 14; Scale/2.10)', 'Patreon/7.6.28 (Android; Android 11; Scale/2.10)']:
        ...
    


class PatreonIE(PatreonBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _RETURN_TYPE = ...


class PatreonCampaignIE(PatreonBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


