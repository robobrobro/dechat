"""Errors and exceptions"""

class NotEncryptedError(Exception):
    """Raised when unencrypted data is used that should have been encrypted."""
    pass
