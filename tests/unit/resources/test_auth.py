from __future__ import absolute_import, unicode_literals

import pytest
import base64
from Crypto.Cipher import DES3
import hashlib

from ravepy.resources.auth import AuthDetails

def test_get_encryption_key(sample_auth_details):
    #implementation details from official web api docs
    seckey = sample_auth_details.secret_key
    hashedseckey = hashlib.md5(seckey.encode("utf-8")).hexdigest()
    hashedseckeylast12 = hashedseckey[-12:]
    seckeyadjusted = seckey.replace('FLWSECK-', '')
    seckeyadjustedfirst12 = seckeyadjusted[:12]
    encryption_key = seckeyadjustedfirst12 + hashedseckeylast12

    #assert our implementation meets theirs
    assert sample_auth_details.encryption_key == encryption_key

def test_encrypt_data(sample_auth_details):
    plain_text = 'ioe98i3g5n9wpn5gw935thq93hpt48hq39848q34ijoiqj4jn4'
    #implementation details from official web api docs
    blockSize = 8
    padDiff = blockSize - (len(plain_text) % blockSize)
    cipher = DES3.new(sample_auth_details.encryption_key, DES3.MODE_ECB)

    new_plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
    encrypted = base64.b64encode(cipher.encrypt(new_plain_text)).decode('utf-8')

    assert sample_auth_details.encrypt_data(plain_text) == encrypted
