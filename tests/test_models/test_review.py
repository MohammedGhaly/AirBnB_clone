#!/usr/bin/python3
"""Contains unittests for models/review.py.

Unittest classes:
    TestReview_save
    TestReview_to_dict
    TestReview_instantiation
"""
import models
import os
from datetime import datetime
import unittest
from models.review import Review
from time import sleep


class TestReview_instantiation(unittest.TestCase):
    """Unittests for instantiation of Review class."""

    def test_no_args_instantiation(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_public_class_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rv))
        self.assertNotIn("place_id", rv.__dict__)

    def test_user_id_public_class_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rv))
        self.assertNotIn("user_id", rv.__dict__)

    def test_text_public_class_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rv))
        self.assertNotIn("text", rv.__dict__)

    def test_2_reviews_unique_ids(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_2_reviews_different_created_at(self):
        rv1 = Review()
        sleep(0.02)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_2_reviews_different_updated_at(self):
        rv1 = Review()
        sleep(0.02)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_str_repr(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rvstr = rv.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_args_not_used(self):
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def test_instantiation_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="3453", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rv.id, "3453")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)

    def test_instantiation_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for save method of Review class."""

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
        rv = Review()
        sleep(0.02)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def test_2_saves(self):
        rv = Review()
        sleep(0.02)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.02)
        rv.save()
        self.assertLess(second_updated_at, rv.updated_at)

    def test_save_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def test_save_updates(self):
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for to_dict method of Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_keys(self):
        rv = Review()
        self.assertIn("created_at", rv.to_dict())
        self.assertIn("id", rv.to_dict())
        self.assertIn("__class__", rv.to_dict())
        self.assertIn("updated_at", rv.to_dict())

    def test_to_dict_added_attributes(self):
        rv = Review()
        rv.middle_name = "Holberton"
        rv.my_number = 100
        self.assertEqual("Holberton", rv.middle_name)
        self.assertIn("my_number", rv.to_dict())

    def test_to_dict_datetime_strs(self):
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertEqual(str, type(rv_dict["updated_at"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["id"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        rv = Review()
        rv.id = "1234567"
        rv.created_at = rv.updated_at = dt
        tdict = {
            'id': '1234567',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(rv.to_dict(), tdict)

    def test_contrast_to_dict_dunder(self):
        rv = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
