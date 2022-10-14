#!/usr/bin/python3
"""
   file testing the file_storage module
"""
import os
import json
import unittest
import uuid
from datetime import datetime
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import remove

class testFileStorage(unittest.TestCase):
    """ the file storage module test class """

    @classmethod
    def setUpClass(cls):
        """FileStorage testing setup.
        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates instances of all class types for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()
        key = "{}.{}".format(type(cls.base).__name__, cls.base.id)
        FileStorage._FileStorage__objects[key] = cls.base
        cls.user = User()
        key = "{}.{}".format(type(cls.user).__name__, cls.user.id)
        FileStorage._FileStorage__objects[key] = cls.user
        cls.state = State()
        key = "{}.{}".format(type(cls.state).__name__, cls.state.id)
        FileStorage._FileStorage__objects[key] = cls.state
        cls.place = Place()
        key = "{}.{}".format(type(cls.place).__name__, cls.place.id)
        FileStorage._FileStorage__objects[key] = cls.place
        cls.city = City()
        key = "{}.{}".format(type(cls.city).__name__, cls.city.id)
        FileStorage._FileStorage__objects[key] = cls.city
        cls.amenity = Amenity()
        key = "{}.{}".format(type(cls.amenity).__name__, cls.amenity.id)
        FileStorage._FileStorage__objects[key] = cls.amenity
        cls.review = Review()
        key = "{}.{}".format(type(cls.review).__name__, cls.review.id)
        FileStorage._FileStorage__objects[key] = cls.review

    @classmethod
    def tearDownClass(cls):
        """FileStorage testing teardown.
        Restore original file.json.
        Delete all test class instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.storage
        del cls.base
        del cls.user
        del cls.state
        del cls.place
        del cls.city
        del cls.amenity
        del cls.review

    def test_file_storage_class_membership(self):
        "checks the instantiation of the file_storage class"
        storage = FileStorage() 
        self.assertIsInstance(storage, FileStorage)

    def test_all_method(self):
        """ checks the file_storage all() method """
        storage = FileStorage()
        self.assertIs(type(storage.all()), dict)

    def test_new_method(self):
        """ test the new method """
        storage = FileStorage()
        dic = {
            'name': "model 1",
            'number': 56,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'id': str(uuid.uuid4())
        }
        storage.new(BaseModel(**dic))
        all_objs = storage.all()
        obj_key = "BaseModel.{}".format(dic['id'])
        self.assertIsInstance(all_objs[obj_key], BaseModel)

    
    def test_reload(self):
        """Test reload method."""
        bm = BaseModel()
        with open("file.json", "w", encoding="utf-8") as f:
            key = "{}.{}".format(type(bm).__name__, bm.id)
            json.dump({key: bm.to_dict()}, f)
        self.storage.reload()
        store = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, store)

    def test_reload_no_file(self):
        """Test reload method with no existing file.json."""
        try:
            self.storage.reload()
        except Exception:
            self.fail

    def test_delete(self):
        """Test delete method."""
        bm = BaseModel()
        key = "{}.{}".format(type(bm).__name__, bm.id)
        FileStorage._FileStorage__objects[key] = bm
        self.storage.delete(bm)
        self.assertNotIn(bm, FileStorage._FileStorage__objects)

    def test_delete_nonexistant(self):
        """Test delete method with a nonexistent object."""
        try:
            self.storage.delete(BaseModel())
        except Exception:
            self.fail
