#!/usr/bin/python3
"""Contains unittests for models/city.py.

Unittest classes:
    TestCity_save
    TestCity_to_dict
    TestCity_instantiation
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for instantiation of City class."""

    def test_no_args_instantiation(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_public_class_attribute(self):
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def test_name_public_class_attribute(self):
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def test_2_cities_unique_ids(self):
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_2_cities_different_created_at(self):
        cy1 = City()
        sleep(0.02)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_2_cities_different_updated_at(self):
        cy1 = City()
        sleep(0.02)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_repr(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_not_used(self):
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="3435", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "3435")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def test_instantiation_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for save method of City class."""

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
        cy = City()
        sleep(0.02)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_2_saves(self):
        cy = City()
        sleep(0.02)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.02)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_arg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates(self):
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for to_dict method of City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_keys(self):
        cy = City()
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("id", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())

    def test_to_dict_added_attributes(self):
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 100
        self.assertEqual("Holberton", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())

    def test_to_dict_datetime_strs(self):
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["updated_at"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["id"]))

    def test_to_dict_out(self):
        dt = datetime.today()
        cy = City()
        cy.id = "1234567"
        cy.created_at = cy.updated_at = dt
        todict = {
            'id': '1234567',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), todict)

    def test_contrast_to_dict_dunder(self):
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_arg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
