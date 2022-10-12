#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name
    Atrr:
        __tablename__(sqlalchemy): rep. the table name
        id(sqlalchemy string): the id column
        name(sqlalchemy string): rep the name column
        state_id(sqlalchemy string): the state id of the city

    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    states = relationship("State", back_populates="city")
