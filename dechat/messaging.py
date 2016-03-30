"""Functions and classes dealing with messaging"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from .errors import *

class Message(object):
    """An encrypted message and its unencrypted metadata."""

    def __init__(self, plaintext, sender, *args, **kwargs):
        """Creates a message.

        Positional arguments:
        plaintext -- plaintext message to encrypt
        sender -- sender of the message
        """

        self.plaintext = plaintext
        self.sender = sender

        # sign the message with the sender's private key
        signer = sender['private_key'].signer(
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA512(),
        )

        signer.update(plaintext.encode('utf-8'))
        self.signature = signer.finalize()

    def encrypt(self, recipient, *args, **kwargs):
        """Encrypts the message intended for recipient.

        Positional arguments:
        recipient -- recipient of the message

        Returns the message after encrypting it.
        """

        self.recipient = recipient

        self.ciphertext = recipient['public_key'].encrypt(
                self.plaintext.encode('utf-8'), 
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
        )

        return self

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

        self.plaintext = recipient['private_key'].decrypt(
                self.ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
        )

        return self

    def serialize(self, *args, **kwargs):
        """Serializes the message.

        If the message is not encrypted, a NotEncryptedError is raised.

        Returns the serialized bytes of the message.
        """

        if not hasattr(self, 'ciphertext'):
            raise NotEncryptedError('Message must be encrypted before serializing')

        # TODO serialize
        message = {
                'signature': self.signature,
                'public_key': self.sender['public_key'],
                'ciphertext': self.ciphertext,
                'recipient': self.recipient['public_key'],
        }

        return message
