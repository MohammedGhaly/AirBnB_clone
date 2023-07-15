#!/usr/bin/python3
"""Contains unittests for models/user.py.

Unittest classes:
    TestUser_save
    TestUser_to_dict
    TestUser_instantiation
"""
import models
import os
from datetime import datetime
import unittest
from models.user import User
from time import sleep


class TestUser_instantiation(unittest.TestCase):
    """Unittests for instantiation of User class."""

    def test_no_args_instantiation(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_2_users_unique_ids(self):
        us2 = User()
        us1 = User()
        self.assertNotEqual(us1.id, us2.id)

    def test_2_users_different_created_at(self):
        us1 = User()
        sleep(0.02)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def test_2_users_different_updated_at(self):
        us1 = User()
        sleep(0.02)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def test_str_repr(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        usstr = us.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def test_args_not_used(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="3345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "3345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def test_instantiation_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for save method of User class."""

    @classmethod
    def setup(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def destroy(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_1_save(self):
        us = User()
        sleep(0.02)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def test_2_saves(self):
        us = User()
        sleep(0.02)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.02)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def test_save_arg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_save_updates(self):
        us = User()
        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for to_dict method of User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_keys(self):
        us = User()
        self.assertIn("created_at", us.to_dict())
        self.assertIn("id", us.to_dict())
        self.assertIn("__class__", us.to_dict())
        self.assertIn("updated_at", us.to_dict())

    def test_to_dict_added_attributes(self):
        us = User()
        us.middle_name = "Holberton"
        us.my_number = 9100
        self.assertEqual("Holberton", us.middle_name)
        self.assertIn("my_number", us.to_dict())

    def test_to_dict_datetime_strs(self):
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["updated_at"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["id"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        us = User()
        us.id = "1234567"
        us.created_at = us.updated_at = dt
        tdict = {
            'id': '1234567',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), tdict)

    def test_contrast_to_dict_dunder(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def test_to_dict_with(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
