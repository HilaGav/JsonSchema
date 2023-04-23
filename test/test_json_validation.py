from src.rest_request_validator import RestRequestValidator
from src.schema_handler import SchemaHandler
from src.types_handler import TypesHandler
import unittest


class TestJsonValidation(unittest.TestCase):
    def setUp(self):
        self.valid_json = open("jsons/valid_json.json", "r")
        self.required_field_error_json = open("jsons/invalid/required_field_error.json", "r")
        self.type_error_json = open("jsons/invalid/type_error.json", "r")
        schema = open("jsons/models.json", "r")
        self.schema_handler = SchemaHandler()
        self.schema_handler.update_schema(schema.read())
        self.type_handler = TypesHandler()

    def test_valid_json_return_true(self):
        json_validate = RestRequestValidator(self.schema_handler, self.type_handler)

        assert len(json_validate.validate_json(self.valid_json.read())) == 0

    def test_invalid_required_json_return_false(self):
        json_validate = RestRequestValidator(self.schema_handler, self.type_handler)

        assert len(json_validate.validate_json(self.required_field_error_json.read())) == 1

    def test_invalid_type_json_return_false(self):
        json_validate = RestRequestValidator(self.schema_handler, self.type_handler)

        assert len(json_validate.validate_json(self.type_error_json.read())) == 1



