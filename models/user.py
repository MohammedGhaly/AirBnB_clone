#!/usr/bin/python3
"""module that contains the 'User' class"""
from models.base_model import BaseModel


class User(BaseModel):
    """class that represents user of an app"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
