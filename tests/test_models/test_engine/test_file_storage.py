#!/usr/bin/python3
"""
   file testing the file_storage module
"""

import unittest
import uuid
from datetime import datetime
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from os import remove

class testFileStorage(unittest.TestCase):
    """ the file storage module test class """

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

    def test_file_storage_save_method(self):
        """FileStorage save method updates __objects
        Test if file already exists.
        with self.assertRaises(FileNotFoundError):
            open('file.json', 'r')
        """
        base = BaseModel()
        key = '{}.{}'.format(type(base).__name__, base.id)
        base_updated_0 = base.updated_at
        storage = FileStorage()
        objs_0 = storage.all()
        dt_0 = objs_0[key].updated_at

        base.save()

        base_updated_1 = base.updated_at
        objs_1 = storage.all()
        dt_1 = objs_1[key].updated_at

        self.assertNotEqual(base_updated_1, base_updated_0)
        self.assertNotEqual(dt_1, dt_0)

        try:
            with open('file.json', 'r'):
                remove('file.json')
        except FileNotFoundError:
            self.assertEqual(1, 2)
