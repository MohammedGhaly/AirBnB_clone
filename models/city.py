#!/usr/bin/python3
"""module containing 'City' class"""
from models.base_model import BaseModel


class City(BaseModel):
    """class representing the city of a room"""
    name = ''
    state_id = ''
