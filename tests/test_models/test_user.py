#!/usr/bin/python3
""" 
    the user.py test module
"""

from models.user import User
from models.base_model import BaseModel
from models import storage
import unittest
import datetime


class testUser(unittest.TestCase):
    """ testing the User class """
    def test_user_membership(self):
        """ tests if obj. is an instance of User class """
        user = User()
        self.assertIsInstance(user, User)

    def test_user_attr_setting(self):
        """ performs check on setting attr. on User """
        my_user = User()
        my_user.first_name = "Foo"
        my_user.last_name = "Bar"
        my_user.email = "airbnb@mail.com"
        my_user.password = "root"
        self.assertEqual(my_user.first_name, "Foo")
        self.assertEqual(my_user.last_name, "Bar")
        self.assertEqual(my_user.email, "airbnb@mail.com")
        self.assertEqual(my_user.password, "root")

    def test_User_attr_type(self):
        """ checks the type of the attributes are correct """
        user = User()
        self.assertEqual(len(user.id), 36)
        self.assertIs(type(user.created_at), datetime.datetime)
        self.assertIs(type(user.updated_at), datetime.datetime)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)

    def test_str_method(self):
        """ test the str method of the base_class """
        user = User()
        string = user.__str__()
        self.assertIsInstance(string, str)

    def test_save_method(self):
        """ tests the save method """
        user = User()
        user.save()
        all_objs = storage.all()
        key = "{}.{}".format("User", user.id)
        self.assertIs(type(all_objs[key]), User)

    def test_to_dict_method(self):
        """ tests the to_dict method of the base class """
        user = User()
        user_dict = user.to_dict()
        self.assertIs(type(user_dict), dict)

    def test_to_dict_key_type(self):
        """ checks the type of key returned from the to_dict method """

        user = User()
        user.first_name = "User 6"
        user.last_name = 83
        m_dict = user.to_dict()
        for key in m_dict.keys():
            self.assertIs(type(key), str)

    def test_to_dict_with_kwargs(self):
        """ test the to_dict method when kwargs is supplied """
        user = BaseModel()
        user.first_name = "User 6"
        user.last_name = 83
        m_dict = user.to_dict()
        model_dict = user.to_dict()
        new_user = User(**model_dict)
        self.assertFalse(new_user is user)
