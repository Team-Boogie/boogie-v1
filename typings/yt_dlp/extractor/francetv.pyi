"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class FranceTVBaseInfoExtractor(InfoExtractor):
    ...


class FranceTVIE(InfoExtractor):
    _VALID_URL = ...
    _GEO_COUNTRIES = ...
    _GEO_BYPASS = ...
    _TESTS = ...


class FranceTVSiteIE(FranceTVBaseInfoExtractor):
    _VALID_URL = ...
    _TESTS = ...


class FranceTVInfoIE(FranceTVBaseInfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


