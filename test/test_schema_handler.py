from src.schema_handler import SchemaHandler
import unittest


class TestSchemaHandler(unittest.TestCase):
    def setUp(self):

        self.schema_handler = SchemaHandler()

    def test_valid_model_return_true(self):
        schema = open("jsons/models.json", "r")

        assert self.schema_handler.update_schema(schema.read())

    def test_invalid_model_return_false(self):
        schema = open("jsons/invalid_models.json", "r")

        assert self.schema_handler.update_schema(schema.read()) is False
