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

    def default(self, line):
        """Default behavior of cmd module"""
        commands = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.count
        }

        dot = re.search(r'\.', line)
        nameclass = line[:dot.span()[0]]
        resteln = line[dot.span()[1]:]

        parenthese = re.search(r'\(.*\)', resteln)
        if parenthese is not None:
            cmd = resteln[:parenthese.span()[0]]
            args = parenthese.group()[1: -1]
            args = "{} [{}]".format(nameclass, args)
            if cmd in commands.keys():
                return commands[cmd](args)
        print("*** Unknown syntax: {}".format(line))

    def do_create(self, line):
        """Usage:create <class>
        Create a new class instance and save it to a JSON file """
        args = self.split(line)

        if len(args) == 1 and args[0] == "":
            print("** class name missing **")
        elif args[0] not in self.__classNames:
            print("** class doesn't exist **")
        else:
            instance = eval(args[0])()
            models.storage.save()
            print(instance.id)

    def do_show(self, line):
        """Prints string representation of class
        instance Usage:show <class> <id>"""

        args = self.split(line)

        if len(args) == 1 and args[0] == "":
            print("** class name missing **")
        elif args[0] not in self.__classNames:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            objects = models.storage.all()

            if key in objects.keys():
                print(objects[key].__str__())
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Delete a class instance of given if
          Usage:destroy <class> <id> """
        args = self.split(line)

        if len(args) == 1 and args[0] == "":
            print("** class name missing **")
        elif args[0] not in self.__classNames:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            objectdict = models.storage.all()

            if key in objectdict.keys():
                del objectdict[key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_update(self, line):
        """Updates a class instance of a given id
          Usage:update <class> <id> <attr> <value>"""
        args = self.split(line)
        objdict = models.storage.all()

        if len(args) == 1 and args[0] == "":
            print("** class name missing **")
        elif args[0] not in self.__classNames:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objdict.keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif args[2][0] == "{":
            obj = objdict["{}.{}".format(args[0], args[1])]
            for key, value in eval(args[2]).items():
                if key in obj.__class__.__dict__.keys():
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(value)
                else:
                    obj.__dict__[key] = value
            obj.__dict__["updated_at"] = datetime.now()
            models.storage.save()
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj = objdict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = value_type(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
            obj.__dict__["updated_at"] = datetime.now()
            models.storage.save()

    def do_count(self, line):
        """Returns the number of class instances"""
        
        args = self.split(line)
        count = 0
        for obj in models.storage.all().values():
             if args[0] == obj.__class__.__name__:
                  count += 1
        print(count)

    @staticmethod
    def split(line):
        """split  arguments"""
        matchiclass = re.search(r' ', line)
        if matchiclass is not None:
            _args = [line[:matchiclass.span()[0]],
                     line[matchiclass.span()[1]:]]
        else:
            _args = [line]
        curlybr = re.search(r'\{.*\}', line)
        brackets = re.search(r'\[.*\]', line)

        args = []

        if curlybr is None:
            if brackets is not None:
                args = brackets.group()[1: -1].split(',')
                args = [arg.strip().strip('"') for arg in args]
            else:
                if len(_args) > 1:
                    args = _args[1].split()
                    args = [arg.strip('"') for arg in args]
        else:
            curlybr = re.search(r'\{.*\}', _args[1])
            args = re.findall(r'[^, ]+', _args[1][:curlybr.span()[0]])
            args = [arg.strip('[').strip('"') for arg in args]
            args.append(curlybr.group())

        args = [arg for arg in args if arg != '']
        args.insert(0, _args[0])
        return args    


if __name__ == '__main__':
    HBNBCommand().cmdloop()
