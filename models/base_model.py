#!/usr/bin/python3
"""
   The base_model module
   Defines a single BaseModel class for initiating the projects objects
"""


import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String


Base = declarative_base()


class BaseModel:

    """
       The base model class
       defines all common attributes/methods for other classes
    Atrr:
        id(sqlalchemy String): the id to be mapped to Basemodel
        created_at(sqlalchemy Datetime): the current datetime at creation
       updated_at(sqlalchemy Datetime): the time updated
    """

    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ Instantiate a new BaseModel """

        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        if kwargs:
            for key, val in kwargs.items():
                if key != '__class__':
                    if key == "created_at" or key == "updated_at":
                        fmt = "%Y-%m-%dT%H:%M:%S.%f"
                        val = datetime.strptime(val, fmt)
                    setattr(self, key, val)

    def __str__(self):
        class_name = self.__class__.__name__
        d = self.__dict__
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(class_name, self.id, d)

    def save(self):
        """
            updates the public instance attribute updated_at
            with the current datetime
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
             returns a dictionary containing all keys/values
             of __dict__ of the instance
        """
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = self.__class__.__name__
        created_at = dictionary["created_at"]
        updated_at = dictionary["updated_at"]
        dictionary["created_at"] = created_at.isoformat()
        dictionary["updated_at"] = updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)

        return dictionary

    def delete(self):
        """ deletes the current instance from the storage """
        models.storage.delete(self)
