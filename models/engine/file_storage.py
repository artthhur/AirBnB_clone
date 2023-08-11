#!/usr/bin/python3
""" Define FileStorage class (serialize/deserialize) """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ represent a storage engine
    Attributes:
        __file_path: name of the file that will contains objects
        __objects: dictionary of objects"""

    __file_path = "SSfile.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file """
        dictObj = {k: self.__objects[k].to_dict()
                     for k in self.__objects.keys()}

        with open(self.__file_path, "w") as f:
            json.dump(dictObj, f)

    def reload(self):
        """ deserializes the JSON file to __objects """
        try:
            with open(self.__file_path, "r") as f:
                objdict = json.load(f)
                for ob in objdict.values():
                    className = ob["__class__"]
                    del ob["__class__"]
                    eval(className)(**ob)
        except FileNotFoundError:
            pass
