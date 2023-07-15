#!/usr/bin/python3
"""Contains unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_save
    TestBaseModel_to_dict
    TestBaseModel_instantiation
"""
import models
import os
from datetime import datetime
import unittest
from models.base_model import BaseModel
from time import sleep


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for instantiation of BaseModel class."""

    def test_no_arg_instantiation(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_2_models_unique_id(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm2.id, bm1.id)

    def test_2_models_different_created_at(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_2_models_different_updated_at(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_not_used(self):
        bmo = BaseModel(None)
        self.assertNotIn(None, bmo.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="3435", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "3435")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_args_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bmo = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bmo.id, "345")
        self.assertEqual(bmo.created_at, dt)
        self.assertEqual(bmo.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for saving method of BaseModel class."""

    @classmethod
    def setup(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        bm = BaseModel()
        sleep(0.1)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_2_saves(self):
        bm = BaseModel()
        sleep(0.03)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.02)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_update_file(self):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for to_dict method of BaseModel class."""

    def test_to_dict_type(self):
        bmodel = BaseModel()
        self.assertTrue(dict, type(bmodel.to_dict()))

    def test_to_dict_keys(self):
        bm = BaseModel()
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("id", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())

    def test_to_dict_attributes(self):
        bm = BaseModel()
        bm.my_number = 98
        bm.name = "Holberton"
        self.assertIn("my_number", bm.to_dict())
        self.assertIn("name", bm.to_dict())

    def test_to_dict_datetime_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_OutPut(self):
        dt = datetime.today()
        bm = BaseModel()
        bm.id = "1234567"
        bm.created_at = bm.updated_at = dt
        todict = {
            'id': '1234567',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), todict)

    def test_contrast_to_dict_dunder(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
