#!/usr/bin/python3
'''contains the "BaseModel" class'''
import uuid
import os
from datetime import datetime
from models import storage


class BaseModel:
    '''a class that defines all common attributes/methods for other classes'''
    def __init__(self, *args, **kwargs):
        '''initializes the object by default or by dict of args'''
        if kwargs:
            for key, value in kwargs.items():
                if not key == '__class__':
                    if key == 'updated_at' or key == 'created_at':
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self) -> str:
        '''changes the returned string on casting the objects to string'''
        return "[{}] ({}) {}".format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        '''changes the last update time of the object (updated_at)'''
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        '''returns the dictionary representation of the object'''
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = type(self).__name__
        new_dict['updated_at'] = self.updated_at.isoformat()
        new_dict['created_at'] = self.created_at.isoformat()
        return new_dict
