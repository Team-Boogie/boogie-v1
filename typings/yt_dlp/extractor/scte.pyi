"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class SCTEBaseIE(InfoExtractor):
    _LOGIN_URL = ...
    _NETRC_MACHINE = ...


class SCTEIE(SCTEBaseIE):
    _WORKING = ...
    _VALID_URL = ...
    _TESTS = ...


class SCTECourseIE(SCTEBaseIE):
    _WORKING = ...
    _VALID_URL = ...
    _TESTS = ...


