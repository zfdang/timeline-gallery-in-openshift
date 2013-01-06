from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
# https://www.dlitz.net/software/python-pbkdf2/
from mypbkdf2 import MyPbkdf2
from types import UnicodeType


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    # algorithm, iterations, salt, hash_val = encoded.split('$', 3)
    # 'pbkdf2_sha256$1000$badd35a96379e68a2692f16d95b1e373$0a1216c91e77d2a1d7a4853a952ed95846246c8dde6cfa6b'
    password = Column(String(120), unique=True)
    photos = relationship("Photo", backref="user")

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.set_password(password)

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

    def __repr__(self):
        return '<User %r>' % (self.name)


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    filename = Column(String(120, convert_unicode=True), unique=True)
    saved_filename = Column(String(180, convert_unicode=True), unique=True)
    url = Column(String(180, convert_unicode=True))
    size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, filename=None, saved_filename=None):
        self.filename = filename
        self.saved_filename = saved_filename

    def __repr__(self):
        return '<Photo %r>' % (self.filename)
