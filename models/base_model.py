#!/usr/bin/python3
"""Defines a class called BaseModel"""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """Class BaseModel of this UBNB project, defines all common
    attributes & methods for other classes
    """

    def __init__(self, *args, **kwargs):
        """Initialise BaseModel attributes
        Arguments:
        args: unsed
        kwargs: Dictionary representation of BaseModel instance
        """

        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            timefrmt = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key == "id":
                    self.id = value
                elif key == "created_at":
                    self.created_at = datetime.strptime(value, timefrmt)
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(value, timefrmt)
                else:
                    self.__dict__[key] = value
        models.storage.new(self)

    def __str__(self):
        """Return string representation of the BaseModel instance"""
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)

    def save(self):
        """update  updated_at with the  current time"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns BaseModel dictionary"""
        BMdict = self.__dict__.copy()
        BMdict["__class__"] = self.__class__.__name__
        BMdict["created_at"] = self.created_at.isoformat()
        BMdict["updated_at"] = self.updated_at.isoformat()
        return BMdict
