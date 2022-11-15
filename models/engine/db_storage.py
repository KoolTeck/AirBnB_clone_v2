#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ defines DBstorage engine using sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        uri = "mysql+mysqldb://{}:{}@{}/{}".format(
            user, passwd,
            host, db
        )
        self.__engine = create_engine(uri, pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ qurries the db in session for all objects
        """
        dic = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            objects = self.__session.query(cls)
            for obj in objects:
                key = "{}.{}".format(
                    obj.__class__.__name__,
                    obj.id
                )
                dic[key] = obj
        else:
            classes = [State, City, Place, Amenity, User, Review]
            for c in classes:
                objects = self.__session.query(c)
                for obj in objects:
                    key = "{}.{}".format(
                        obj.__class__.__name__,
                        obj.id
                    )
                    dic[key] = obj
        return dic

    def new(self, obj):
        """
        adds the obj to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all change in the session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes from current db session

        obj: the object to delete
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all table in the db """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ closses the current db session """
        self.__session.close()
