"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class RCSBaseIE(InfoExtractor):
    _UUID_RE = ...
    _RCS_ID_RE = ...
    _MIGRATION_MAP = ...


class RCSEmbedsIE(RCSBaseIE):
    _VALID_URL = ...
    _EMBED_REGEX = ...
    _TESTS = ...
    _WEBPAGE_TESTS = ...


class RCSIE(RCSBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class RCSVariousIE(RCSBaseIE):
    _VALID_URL = ...
    _TESTS = ...


