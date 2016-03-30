""" Functions dealing with user data """

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

class User(dict):
    """A user and its data"""

    def __init__(self, password, private_key, public_key, *args, **kwargs):
        """Creates user data.

        Positional arguments:
        password -- password used to symmetrically encrypt the private key
        private_key -- the user's private key
        public_key -- the user's public key
        """

        self['password'] = bytes(password.encode('utf-8'))
        self['private_key'] = private_key
        self['public_key'] = public_key
   
    @classmethod
    def create(cls, password, *args, **kwargs):
        """Creates user data.
    
        Positional arguments:
        password -- password used to symmetrically encrypt the private key
    
        Returns a user.
        """

        private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=default_backend(),
        )

        return User(password, private_key, private_key.public_key())
    
    @classmethod
    def load(cls, data, password, *args, **kwargs):
        """Loads a user from serialized data.

        Positional arguments:
        data -- serialized user data
        password -- password to decrypt the user's private key

        Returns a user.
        """

        private_key = serialization.load_pem_private_key(
                data['private_key'],
                password=bytes(password.encode('utf-8')),
                backend=default_backend(),
        )

        public_key = serialization.load_pem_public_key(
                data['public_key'],
                backend=default_backend(),
        )

        return User(password, private_key, public_key)

    def serialize(self, *args, **kwargs):
        """Serializes the user's data."""

        private_key_pem = self['private_key'].private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(self['password']),
        )

        public_key_pem = self['public_key'].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return {
                'private_key': private_key_pem,
                'public_key': public_key_pem,
        }

    def sign(self, message, *args, **kwargs):
        """Signs a message.

        Positional arguments:
        message -- the message to sign
        """

        # sign the message with the sender's private key
        signer = self['private_key'].signer(
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA512(),
        )

        signer.update(message.payload.encode('utf-8'))
        message.signature = signer.finalize()

    def verify(self, message, *args, **kwargs):
        """Verifies the signature in a message.

        Positional arguments:
        message -- the message to verify

        Raises InvalidSignature if the verification fails.
        """

        verifier = self['public_key'].verifier(
                message.signature,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA512(),
        )

        verifier.update(message.payload.encode('utf-8'))
        verifier.verify()

def create_user(password, *args, **kwargs):
    """Creates user data.
    
    Positional arguments:
    password -- password used to symmetrically encrypt the private key
   
    Returns a user.
    """

    return User.create(password, *args, **kwargs)

def load_user(data, password, *args, **kwargs):
    """Loads a user from serialized data.

    Positional arguments:
    data -- serialized user data
    password -- password to decrypt the user's private key

    Returns a user.
    """

    return User.load(data, password, *args, **kwargs)
