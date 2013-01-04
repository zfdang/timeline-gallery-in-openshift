from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

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

    def __init__(self, filename=None, saved_filename=None):
        self.filename = filename
        self.saved_filename = saved_filename

    def __repr__(self):
        return '<User %r>' % (self.filename)
