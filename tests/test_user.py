"""Tests dealing with the user module"""

from dechat.user import *
from nose.tools import *

@raises(AttributeError, ValueError)
def test_serialize_password_is_none(*args, **kwargs):
    user = create_user(None)
    data = user.serialize()

@raises(ValueError)
def test_serialize_password_is_empty(*args, **kwargs):
    user = create_user('')
    data = user.serialize()

def test_serialize_and_load(*args, **kwargs):
    user = create_user('x')
    data = user.serialize()
    ok_('private_key' in data)
    ok_('public_key' in data)
    ok_('password' not in data)
    user2 = load_user(data, 'x')
    data2 = user2.serialize()
    eq_(data['public_key'], data2['public_key'])
