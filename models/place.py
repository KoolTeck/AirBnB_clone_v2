#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
import models
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Integer
from sqlalchemy import ForeignKey, Float, Table
from sqlalchemy.orm import relationship


association_table = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60), ForeignKey("places.id"),
        primary_key=True, nullable=False
        ),
    Column(
        "amenity_id",
        String(60), ForeignKey("amenities.id"),
        primary_key=True, nullable=False
        )
)


class Place(BaseModel, Base):
    """ The place class mapping """
    __tablename__ = "places"
    city_id = Column(
        String(60),
        ForeignKey("cities.id"),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        nullable=False
    )
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(
        Integer,
        default=0
    )
    number_bathrooms = Column(
        Integer,
        default=0
    )
    max_guest = Column(
        Integer,
        default=0
    )
    price_by_night = Column(
        Integer,
        default=0
    )
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship(
        "Review", backref="place",
        cascade="delete")
    amenities = relationship(
        "Amenity", secondary="place_amenity",
        viewonly=False)

    if (getenv("HBNB_TYPE_STORAGE") != 'db'):
        @property
        def reviews(self):
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """
            returns a list of amenities linked to the places class
            """
            amenities_list = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, value):
            """ sets amenity id in the attribut amenity_ids """
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
