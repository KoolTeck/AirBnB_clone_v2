#!/usr/bin/python3
""" Tests suits for console.py """
import os
import unittest
from io import StringIO
from unittest.mock import patch
import models
from models.engine.file_storage import FileStorage
from console import HBNBCommand
import pep8


class TestHBNBCommand(unittest.TestCase):
    """ defines test cases for HBNBCommand console """
    @classmethod
    def setUpClass(cls):
        """ Setting the commamd testing setup
        rename the initial file
        create an instance of the class
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """ command testing teardown.

        restores the initial json file.
        deletes the class instance
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        del cls.HBNB

    def setUp(self):
        """ Resets the file storage obj dict """
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """ Deletes created file.json"""
        try:
            os.remove('file.json')
        except IOError:
            pass

    def test_pep8(self):
        """ checks pep8 style guide """
        style = pep8.StyleGuide(quite=True)
        check = style.check_files(["console.py"])
        self.assertEqual(check.total_errors, 0, "pep8 fix")

    def test_docstrings(self):
        """ check for docstrings """
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)


    def test_empty_input(self):
        """ checks empty command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('\n')
            self.assertEqual("", f.getvalue())

    def test__quit(self):
        """ checks quit command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('quit')
            self.assertEqual("", f.getvalue())

    def test__EOF(self):
        """ checks EOF command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('EOF')
            self.assertEqual("", f.getvalue())

    def test_create_error_input(self):
        """ checks for error input of the create command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create')
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create abcdgibberrish')
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == "DbStorage", "Now testing DBS")
    def test_create_without_param(self):
        """Test the create command without param """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            us = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            st = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Place")
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create City")
            ct = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Review")
            rv = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Amenity")
            am = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(bm, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            self.assertIn(us, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(st, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            self.assertIn(pl, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all City")
            self.assertIn(ct, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Review")
            self.assertIn(rv, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(am, f.getvalue())

    def test_create_with_kwargs_param(self):
        """ Test create command with kwargs """
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = ('create Place city_id="0001" '
                'user_id="0001" name="My_little_house" '
                'number_rooms=4 number_bathrooms=2 '
                'max_guest=10 price_by_night=300 '
                'latitude=37.773972 longitude=-122.431297')
            self.HBNB.onecmd(cmd)
            state1 = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            place_objs = f.getvalue()
            self.assertIn(state1, place_objs)
            self.assertIn("'city_id': '0001'", place_objs)
            self.assertIn("'name': 'My little house'", place_objs)
            self.assertIn("'number_rooms': '4'", place_objs)
            self.assertIn("'number_bathrooms': '2'", place_objs)
            self.assertIn("'max_guest': '10'", place_objs)
            self.assertIn("'price_by_night': '300'", place_objs)
            self.assertIn("'latitude': '37.773972'", place_objs)
            self.assertIn("'longitude': '-122.431297'", place_objs)
            
