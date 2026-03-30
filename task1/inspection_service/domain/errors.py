class InspectionError(Exception):
    """Base error for inspection domain."""


class FileValidationError(InspectionError):
    """Raised when the input file path is invalid."""


class UnsupportedImageFormatError(InspectionError):
    """Raised when image extension is not supported."""


class InspectionTimeoutError(InspectionError):
    """Raised when model prediction exceeds timeout."""


class DetectorError(InspectionError):
    """Raised when detector fails for any other reason."""
