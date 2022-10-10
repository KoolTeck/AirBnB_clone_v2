#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class tesBaseModel(unittest.TestCase):
    """The base_model file test suites """

    def test_base_class_membership(self):
        """ tests if obj. is an instance of base_class """
        model_1 = BaseModel()
        self.assertIsInstance(model_1, BaseModel)

    
    def test_base_class_attr_setting(self):
        """ test setting attribute on the base class """
        model_2 = BaseModel()
        model_2.name = "My name changed"
        model_2.my_number = 81
        
        self.assertEqual(model_2.name, "My name changed")
        self.assertEqual(model_2.my_number, 81)

    def test_str_method(self):
        "u"" test the str method of the base_class """
        model3 = BaseModel()
        string = model3.__str__()
        self.assertIsInstance(string, str)

    def test_save_method(self):
        """ tests the save method """
        model4 = BaseModel()
        model4.name = "Model 4"
        model4.my_number = 82
        current_time  = model4.updated_at
        model4.save()
        self.assertNotEqual(current_time, model4.updated_at)
        
    def test_to_dict_method(self):
        """ tests the to_dict method of the base class """
        model5 = BaseModel()
        model_dict = model5.to_dict()
        self.assertIs(type(model_dict), dict)
        self.assertEqual(model_dict['id'], model5.id)
        self.assertEqual(model_dict['__class__'], type(model5).__name__)
        self.assertEqual(model_dict['created_at'], model5.created_at.isoformat())
        self.assertEqual(model_dict['updated_at'], model5.updated_at.isoformat())
        self.assertIsInstance(model5.created_at, datetime.datetime)
        self.assertIsInstance(model5.updated_at, datetime.datetime)

    def test_to_dict_key_type(self):
        """ checks the type of key returned from the to_dict method """
        
        model6 = BaseModel()
        m_dict = model6.to_dict()
        for key in m_dict.keys():
            self.assertIs(type(key), str)

    def test_to_dict_with_kwargs(self):
        """ test the to_dict method when kwargs is supplied """
        model8 = BaseModel()
        model8.name = "Model 8"
        model8.my_number = 84
        model_dict = model8.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertFalse(new_model is model8)

    def test_to_dict_updated_at_and_created_at_kwarg_key(self):
        """ checks the return value of the updated and created_at key when using kwargs on the method """
        model9 = BaseModel()
        model9.name = "model 9"
        model9.my_number = 85
        model_dict = model9.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertIs(type(new_model.created_at), datetime.datetime)
        self.assertIs(type(new_model.updated_at), datetime.datetime)
