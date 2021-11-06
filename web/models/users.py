import uuid

from sqlalchemy import Column, String

from web import db
from web.utils import Hash


class User(db.Model):
    __tablename__ = "users"
    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(400), nullable=False)

    def __init__(self, name, username, email, password):
        self.id = str(uuid.uuid4().hex)
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = Hash.bcrypt(password)
