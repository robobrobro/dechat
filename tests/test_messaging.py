"""Tests for messaging"""

from dechat.errors import NotEncryptedError
from dechat.user import create_user, load_user
from dechat.messaging import *
from nose.tools import *

def test_ctor_valid_user(*args, **kwargsg):
    user = create_user('password')
    msg = Message('test', user)
    eq_('test', msg.plaintext)
    eq_(512, len(msg.signature))

@raises(NotEncryptedError)
def test_decrypt_unencrypted_message(*args, **kwargs):
    user = create_user('password')
    msg = Message('test', user)
    msg.decrypt(user)

def test_encrypt_and_decrypt(*args, **kwargs):
    sender = create_user('password')
    msg = Message('test', sender)
    recipient = create_user('1337')
    msg.encrypt(recipient)
    msg.decrypt(recipient)
    eq_('test'.encode('utf-8'), msg.plaintext)

def test_encrypt_serialize_load_and_decrypt(*args, **kwargs):
    sender = create_user('password')
    msg = Message('test', sender)
    recipient = create_user('1337')
    msg.encrypt(recipient)
    recipient_data = recipient.serialize()
    recipient = load_user(recipient_data, '1337')
    msg.decrypt(recipient)
    eq_('test'.encode('utf-8'), msg.plaintext)

@raises(NotEncryptedError)
def test_serialize_unencrypted_message(*args, **kwargs):
    user = create_user('password')
    msg = Message('test', user)
    msg.serialize(user)

def test_serialize_encrypted_message(*args, **kwargs):
    user = create_user('password')
    msg = Message('test', user)
    msg.encrypt(user)
    data = msg.serialize(user)
    ok_('plaintext' not in data)
    ok_('signature' in data)
    ok_('ciphertext' in data)
