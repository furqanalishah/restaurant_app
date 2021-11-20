import uuid

from sqlalchemy import Column, String, TEXT

from web import db


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    halal_foods = Column(TEXT, nullable=False)
    location_name = Column(String(100), nullable=False)
    latitude = Column(String(30), nullable=False)
    longitude = Column(String(30), nullable=False)

    def __init__(self, name, email, halal_foods, location_name, latitude, longitude):
        self.id = str(uuid.uuid4().hex)
        self.location_name = location_name
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.email = email
        self.halal_foods = halal_foods

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location_name": self.location_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "email": self.email,
            "halal_foods": self.halal_foods,
        }
