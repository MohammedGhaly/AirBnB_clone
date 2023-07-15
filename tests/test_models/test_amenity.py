#!/usr/bin/python3
"""contains unittests for models/amenity.py.

Unittest classes:
    TestAmenity_save
    TestAmenity_to_dict
    TestAmenity_instantiation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for instantiation of Amenity class."""

    def test_no_args_instantiation(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_public_class_attribute(self):
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_2_amenities_unique_ids(self):
        am2 = Amenity()
        am1 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_two_amenities_different_created_at(self):
        am1 = Amenity()
        sleep(0.02)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_two_amenities_different_updated_at(self):
        am1 = Amenity()
        sleep(0.02)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_repr(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_not_used(self):
        amen = Amenity(None)
        self.assertNotIn(None, amen.__dict__.values())

    def test_instantiation_kwargs(self):
        """instantiation kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="3435", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "3435")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def test_instantiation_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for saving method of Amenity class."""

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
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_2_saves(self):
        am = Amenity()
        sleep(0.02)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.02)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_save_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def test_save_updates(self):
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for to_dict method of Amenity class."""

    def test_to_dict(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_keys(self):
        am = Amenity()
        self.assertIn("created_at", am.to_dict())
        self.assertIn("id", am.to_dict())
        self.assertIn("__class__", am.to_dict())
        self.assertIn("updated_at", am.to_dict())

    def test_to_dict_added_attributes(self):
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 100
        self.assertEqual("Holberton", am.middle_name)
        self.assertIn("my_number", am.to_dict())

    def test_to_dict_datetime_strs(self):
        am = Amenity()
        am_dict = am.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        am = Amenity()
        am.id = "1234567"
        am.created_at = am.updated_at = dt
        todict = {
            'id': '1234567',
            '__class__': 'Amenity',
            'updated_at': dt.isoformat(),
            'created_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), todict)

    def test_contrast_to_dict_dunder(self):
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
