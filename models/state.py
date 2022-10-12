#!/usr/bin/python3
"""
   The state module
"""
import models
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """
    the state class
    Attr:
        name: string - state's name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

@property
def cities(self):
    """ returns a list of City instances with state_id equals to the current State.id
    """
    city_list = []
    for city in models.storage.all("City").values():
        if city.state_id == self.id:
            city_list.append(city)
    return city_list
