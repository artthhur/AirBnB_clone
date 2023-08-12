#!/usr/bin/python3
"""define the hbnb command interpreter"""
import cmd
from datetime import datetime
import re
from shlex import split
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter Class"""
    prompt = '(hbnb) '
    __classNames = ["BaseModel",
                    "User",
                    "State",
                    "City",
                    "Amenity",
                    "Place",
                    "Review"]

    def do_EOF(self, line):
        """Exit the program when EOF or  CTRL+D"""
        print()
        return True

    def do_quit(self, line):
        """Quit command  to exit the program"""
        return True
    def emptyline(self):
        """Do nothing when receiving an empty line"""
        pass



if __name__ == '__main__':
    HBNBCommand().cmdloop()
