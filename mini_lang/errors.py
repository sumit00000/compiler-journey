"""
Custom MiniLang exceptions.
"""


class MiniLangError(Exception):
    """Base exception."""
    pass


class LexerError(MiniLangError):
    pass


class ParserError(MiniLangError):
    pass


class RuntimeError(MiniLangError):
    pass