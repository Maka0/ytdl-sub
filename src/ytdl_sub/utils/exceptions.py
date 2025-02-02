class ValidationException(ValueError):
    """Any user-caused configuration error should result in this error"""


class StringFormattingException(ValidationException):
    """Tried to format a string but failed due to user misconfigured variables"""


class StringFormattingVariableNotFoundException(StringFormattingException):
    """Tried to format a string but the variable was not found"""


class DownloadArchiveException(ValueError):
    """Any user or file errors caused by download archive or mapping files"""


class FileNotFoundException(ValidationException):
    """Any user file that's expected to exist, but is not found"""


class InvalidYamlException(ValidationException):
    """User yaml that is invalid"""
