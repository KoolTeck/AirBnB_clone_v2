#!/usr/bin/python3
"""
    the state.py test module
"""

from models.state import State
from models.base_model import BaseModel
from models import storage
import unittest
import datetime


class testUser(unittest.TestCase):
    """ testing the User class """
    def test_user_membership(self):
        """ tests if obj. is an instance of State class"""
        state = State()
        self.assertIsInstance(state, State)

    def test_state_attr_setting(self):
        """ performs check on setting attr. on User """
        state = State()
        state.name = "Foo"
        self.assertEqual(state.name, "Foo")

    def test_attr_type(self):
        """ checks the type of the attributes are correct """
        state = State()
        self.assertIsNotNone(state.name)

    def test_str_method(self):
        """ test the str method of the base_class """
        state = State()
        string = state.__str__()
        self.assertIsInstance(string, str)
    
    def test_save_method(self):
        """ tests the save method """
        state = State()
        state.save()
        all_objs = storage.all()
        key = "{}.{}".format("State", state.id)
        self.assertIs(type(all_objs[key]), State)

    def test_to_dict_method(self):
        """ tests the to_dict method """
        state = State()
        state_dict = state.to_dict()
        self.assertIs(type(state_dict), dict)
