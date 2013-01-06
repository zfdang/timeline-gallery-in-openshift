import binascii
import hashlib
import os
# http://pypi.python.org/pypi/simple-pbkdf2/1.0
from pbkdf2 import pbkdf2_hex


def safe_str_cmp(a, b):
    if len(a) != len(b):
        return False
    rv = 0
    for x, y in zip(a, b):
        rv |= ord(x) ^ ord(y)
    return rv == 0


class MyPbkdf2(object):
    """docstring for MyPbkdf2
    def set_password(self, password):
        if isinstance(password, UnicodeType):
            password = password.encode("UTF-8")
        pbkdf2 = MyPbkdf2()
        self.password = pbkdf2.make_password(password)

    def check_password(self, password):
        if isinstance(password, UnicodeType):
            password = password.encode("UTF-8")
        pbkdf2 = MyPbkdf2()
        return pbkdf2.check_password(password, self.password)
    """
    hashfunc = hashlib.sha256
    iterations = 1000
    saltlen = 16
    keylen = 24

    def __init__(self, iterations=1000, saltlen=16, keylen=24):
        self.iterations = iterations
        self.saltlen = saltlen
        self.keylen = keylen

    def check_password(self, password, encoded):
        algorithm, iterations, salt, hash_val = encoded.split('$', 3)
        assert algorithm == "pbkdf2_sha256"
        #expected = pbkdf2_hex(password, salt, int(iterations), hashfunc=self.hashfunc)
        expected = self.make_password(password, salt, int(iterations))
        return safe_str_cmp(encoded, expected)

    def make_password(self, password, salt=None, iterations=None):
        if not salt:
            salt = self.generate_salt()
        if not iterations:
            iterations = self.iterations
        hash_val = pbkdf2_hex(password, salt, iterations, hashfunc=self.hashfunc, keylen=self.keylen)
        return '%s$%s$%s$%s' % ('pbkdf2_sha256', iterations, salt, hash_val)

    def generate_salt(self):
        return binascii.b2a_hex(os.urandom(self.saltlen))
