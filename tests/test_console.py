#!/usr/bin/python3
""" Tests suits for console.py """
import os
import unittest
from io import StringIO
from unittest.mock import patch
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
            os.rename("file.json", tmp)
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
            os.rename("file.json", tmp)
        except IOError:
            pass
        del cls.HBNB

    def setUp(self):
        """ Resets the file storage obj dict """
        FileStorage._FileStorage.__objects = {}

    def tearDown(self):
        """ Deletes created file.json"""
        try:
            os.remove('file.json')
        except IOError:
            pass

    def test_pep8(self):
        """ checks pep8 style guide """
        style = pep8.StyleGuide(quite=True)
        check = style.check_files("console.py")
        self.assertEqual(check.total_errors, 0, "pep8 fix")

    def test_docstrings(self):
        """ check for docstrings """
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update_.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)


    def test_empty_input(self):
        """ checks empty command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('\n')
            self.assertEqual("", f.getvalue)

    def test__quit(self):
        """ checks quit command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('quit')
            self.assertEqual("", f.getvalue)

    def test__EOF(self):
        """ checks EOF command """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('EOF')
            self.assertEqual("\n", f.getvalue)
