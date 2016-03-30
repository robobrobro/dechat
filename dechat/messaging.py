"""Functions and classes dealing with messaging"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from .errors import *
import json

class Message(object):
    """A message."""

    def __init__(self, payload, *args, **kwargs):
        """Creates a message.

        Positional arguments:
        payload -- the payload of the message
        """

        self.payload = payload

    def serialize(self, sender, recipient, *args, **kwargs):
        """Serializes the message.

        Positional arguments:
        sender -- sender of the message
        recipient -- recipient of the message

        Returns the message after serializing it.

        Raises a NotSignedError if the message is not signed.
        """

        if not hasattr(self, 'signature') or self.signature is None:
            raise NotSignedError('Cannot serialize an unsigned message')

        self.sender = sender
        self.recipient = recipient

        message = {
                'signature': self.signature,
                'public_key': self.sender['public_key'],
                'payload': self.payload,
                'recipient': self.recipient['public_key'],
        }

        self.plaintext = json.dumps(message)

        return self

    def encrypt(self, *args, **kwargs):
        """Encrypts the message intended for recipient.

        Returns the encrypted bytes of the message.

        Raises a NotSerializedError if the message is not serialized.
        """

        if not hasattr(self, 'plaintext') or self.plaintext is None:
            raise NotSerializedError('Cannot encrypt an unserialized message')

        ciphertext = self.recipient['public_key'].encrypt(
                self.plaintext, 
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
        )

        return ciphertext

    def decrypt(self, recipient, *args, **kwargs):
        """Decrypts the message intended for recipient.

        Raises a NotEncryptedError if the message is not encrypted.

        Positional arguments:
        recipient -- recipient of the message

        Returns the message after decrypting it.
        """

        if not hasattr(self, 'ciphertext'):
            raise NotEncryptedError('Cannot decrypt a unecrypted message')

        self.recipient = recipient

        self.payload = recipient['private_key'].decrypt(
                self.ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
        )

        return self

