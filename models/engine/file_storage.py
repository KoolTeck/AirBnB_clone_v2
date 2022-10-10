#!/usr/bin/python3
"""
    The file_storage module
    provides a single class FileStorage
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """ serializes instances to a JSON file
        and deserializes JSON file to instances
        Attributes:
                   __file_path(str): the file to serialize instance into
                   __objects(dict): the dictionary of objs
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        if obj:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        obj_dict = {}
        for key, val in self.__objects.items():
            obj_dict[key] = val.to_dict()

        obj_json_str = json.dumps(obj_dict)
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            f.write(obj_json_str)

    def reload(self):
        """ deserializes the JSON file to __objects """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                obj_json = json.load(f)

            for obj_dic in obj_json.values():
                cls = obj_dic['__class__']
                cls = eval(cls)
                self.new(cls(**obj_dic))
        except FileNotFoundError:
            pass
