"""Errors and exceptions"""

class NotEncryptedError(Exception):
    """Raised when unencrypted data is used that should have been encrypted."""
    pass

class NotSerializedError(Exception):
    """Raised when a message is not serialized."""
    pass

class NotSignedError(Exception):
    """Raised when a message is not signed."""
    pass
