#!/usr/bin/python3
'''module containing the FileStorage class'''
import json
import os
import datetime
import re


class FileStorage:
    '''
    serializes instances into a JSON files
    and deserializes JSON files into instances
    '''

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        '''returns the dictionary of objects'''
        return FileStorage.__objects

    def new(self, obj):
        '''
        adds object (obj) to the dictionary
        key: object_type.object_id, ex: BaseModel.1234
        '''
        key = f'{type(obj).__name__}.{obj.id}'
        FileStorage.__objects[key] = obj

    def save(self):
        '''
        saves JSON represenation of objects to the data file
        '''
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json_dict = {
                    key: value.to_dict() for key, value in FileStorage.
                    __objects.items()
                    }
            json.dump(json_dict, f)

    def reload(self):
        '''
        deserializes the JSON file to __objects
        '''
        if not os.path.isfile(FileStorage.__file_path):
            return
        regex = r'^([a-zA-Z])*'

        with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
            objs_dict = json.load(f)
            FileStorage.__objects = {
                k: self.classes()[re.match(regex, k).group(0)](**v)
                for k, v in objs_dict.items()
                }

    def classes(self):
        '''
        returns a dictionary of available classes
        key: class name (string)
        value: class (class)
        '''
        from models.base_model import BaseModel
        from models.user import User
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.state import State
        from models.review import Review
        models = {
            "BaseModel": BaseModel,
            "User": User,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "State": State,
            "Review": Review
        }
        return models

    def attributes(self):
        """Returns available attributes and their types for each class name"""
        attrs = {
            "BaseModel":
                {"id": str,
                 "updated_at": datetime.datetime,
                 "created_at": datetime.datetime},
            "Place":
                {"city_id": str,
                 "number_bathrooms": int,
                 "longitude": float,
                 "number_rooms": int,
                 "name": str,
                 "price_by_night": int,
                 "max_guest": int,
                 "description": str,
                 "user_id": str,
                 "latitude": float,
                 "amenity_ids": list},
            "State":
                {"name": str},
            "User":
                {"email": str,
                 "first_name": str,
                 "last_name": str,
                 "password": str},
            "Amenity":
                {"name": str},
            "City":
                {"state_id": str,
                 "name": str},
            "Review":
                {"place_id": str,
                 "text": str,
                 "user_id": str}
        }
        return attrs
