#!/usr/bin/python3
import os
from datetime import datetime
import inspect
import unittest
from unittest.mock import MagicMock
import pycodestyle

import models
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def setUp(self) -> None:
        """
        Set up resources required for each test method.
        """
        self.model = BaseModel()
        # mocking to isolate save method of BaseModel
        # with new and save_obj of filestorage
        self.mock_save = MagicMock()
        models.storage.save = self.mock_save
        self.mock_new = MagicMock()
        models.storage.new = self.mock_new

    def tearDown(self) -> None:
        """
        Teardown method to clean up resources after each test method.
        """
        del self.model

    # Custom Methods

    def assert_hasattri(self, model, attribute) -> None:
        """
        Custom assert_hasattri Method.
        """
        self.assertTrue(hasattr(model, attribute),
                        f'{model} Attribute {attribute} does not exist')

    def assert_attribute_match(self, model, model_attribute) -> None:
        """
        Custom match object attribute after
        reloading to ensure attribute uniqueness.
        """
        self.assertEqual(model, model_attribute,
                         f"{model_attribute} don't match ")

    def assert_attribute_instance_types(self, model,
                                        attribute_dict: dict) -> None:
        """
        Custom assertIsinstance
        """
        for attribute_name, attribute_type in attribute_dict.items():
            self.assertIsInstance(model[attribute_name], attribute_type,
                                  f"Attribute {attribute_name} "
                                  f"not {attribute_type} instance")

    # Test Methods

    def test_module_and_BaseModel_doc_string(self) -> None:
        """
        Responsible for checking for baseModel
        and base_model file docstring.
        """
        # baseModel file  and BaseModel class docstring
        self.assertIsNotNone(models.base_model.__doc__,
                             f'Module {models.base_model} has no docstring')
        self.assertIsNotNone(BaseModel.__doc__,
                             'BaseModel class has no docstring')

    def test_all_BaseModel_methods_doc_string(self) -> None:
        """
        Responsible for checking all BaseModel Method docstring.
        """
        BaseModel_method = inspect.getmembers(self.model,
                                              inspect.ismethod)
        for name, method in BaseModel_method:
            self.assertIsNotNone(method.__doc__,
                                 f"Method <{name}> of BaseModel"
                                 f" has no docstring")

    def test_pep8Compliance(self):
        style_guide = pycodestyle.StyleGuide()
        test_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(test_dir,
                                 "../../models/base_model.py")
        report = style_guide.check_files([file_path])
        self.assertEqual(report.total_errors, 0,
                         f"PEP8 violations found:"
                         f" {report.total_errors}")

    def test_init_method(self) -> None:
        """
        Responsible for testing __init__ method
        """
        # check if model has attributes
        self.assert_hasattri(self.model, 'id')
        self.assert_hasattri(self.model, 'created_at')
        self.assert_hasattri(self.model, 'updated_at')
        # check attribute instances
        self.assert_attribute_instance_types(self.model.__dict__,
                                             {'id': str,
                                              'created_at': datetime,
                                              'updated_at': datetime})

    def test_custom_init_method(self) -> None:
        """
        Responsible for testing the __init__ method when objects are reloaded.
        """
        model_json = self.model.to_dict()
        model_dict = BaseModel(**model_json)  # custom reload_object

        # check reloaded object is BaseModel instance
        self.assertIsInstance(model_dict, BaseModel,
                              "Deserialized object is "
                              "not an instance of BaseModel")
        self.assertIsInstance(model_json, dict, f'{model_json} '
                                                f'is not a dict instance')

        # created_at and updated_at are datetime instance
        self.assert_attribute_instance_types(self.model.__dict__,
                                             {'created_at': datetime,
                                              'updated_at': datetime})

        # reloaded_object attribute match with the original object attribute.
        self.assert_attribute_match(self.model.id, model_dict.id)
        self.assert_attribute_match(self.model.created_at,
                                    model_dict.created_at)
        self.assert_attribute_match(self.model.updated_at,
                                    model_dict.updated_at)

    def test_str_method(self) -> None:
        """
        Responsible for testing BaseModel __str__ Method.
        """
        # expected string format
        expected_str = "[{}] ({}) {}".format(
            self.model.__class__.__name__,
            self.model.id,
            self.model.__dict__
        )

        # string match
        self.assertEqual(self.model.__str__(), expected_str,
                         "strings don't match")

    def test_save_method(self) -> None:
        """
        Responsible for testing BaseModel save Method.
        """
        model_updated_at = self.model.updated_at

        # call the BaseModel save method.
        self.model.save()

        # update object updated_at
        updated_model_time = self.model.updated_at

        # check if the save method updated the BaseModel updated_at time.
        self.assertNotEqual(model_updated_at, updated_model_time,
                            "Attribute updated_at did not update"
                            " the created_at time")

        # mocking to isolate save method with new
        # and save_obj of filestorage
        self.mock_save.assert_called_once()  # save_obj
        # of filestorage called once

    def test_to_dict_method(self) -> None:
        """
        Responsible for testing BaseModel to_dict Method.
        """
        # Arrange: Convert object to dictionary format
        model_json = self.model.to_dict()

        # Assert: Check if the conversion is correct
        self.assertIsInstance(model_json, dict,
                              'Object not a dict instance')
        self.assertIn('__class__', model_json,
                      "__class__ not present in dictionary")
        # Check instance types
        self.assert_attribute_instance_types(model_json,
                                             {'created_at': str,
                                              'updated_at': str})
        self.assert_attribute_instance_types(self.model.__dict__,
                                             {'created_at': datetime,
                                              'updated_at': datetime})


if __name__ == '__main__':
    unittest.main()
