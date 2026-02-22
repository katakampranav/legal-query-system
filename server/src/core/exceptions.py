"""Custom exceptions for the application."""


class RevealingException(Exception):
    """Base exception for the application."""

    pass


class LLMException(RevealingException):
    """Raised when LLM API call fails."""

    pass


class RetrieverException(RevealingException):
    """Raised when document retrieval fails."""

    pass


class ValidationException(RevealingException):
    """Raised when input validation fails."""

    pass


class ConfigException(RevealingException):
    """Raised when configuration is invalid."""

    pass
