class InsightError(Exception):
    """Base error for insight domain."""


class LlmUnavailableError(InsightError):
    """Raised when LLM is not available or fails."""
