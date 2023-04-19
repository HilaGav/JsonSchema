from src.JsonValidator import JsonValidator
from src.SchemaHandler import SchemaHandler


def test_validate_json():
    # Test schema for an object with two required properties
    schema = '''
    {
        "type": "object",
        "required": ["name", "age"],
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"}
        }
    }
    '''

    # Valid JSON data
    json_data_valid = '{"name": "Alice", "age": 30}'
    assert JsonValidator.validate_json(json_data_valid, schema)

    # Invalid JSON data missing a required property
    json_data_invalid = '{"name": "Bob"}'
    assert JsonValidator.validate_json(json_data_invalid, schema)

    # Valid JSON data with an additional property
    json_data_additional = '{"name": "Charlie", "age": 25, "city": "New York"}'
    assert JsonValidator.validate_json(json_data_additional, schema) == True

    # Valid JSON data for an array of numbers
    schema_array = '{"type": "array", "items": {"type": "number"}}'
    json_data_array_valid = '[1, 2, 3, 4, 5]'
    assert JsonValidator.validate_json(json_data_array_valid, schema_array)

    # Invalid JSON data for an array of numbers with a string value
    json_data_array_invalid = '[1, 2, "three", 4, 5]'
    assert not JsonValidator.validate_json(json_data_array_invalid, schema_array)

def test_validate_json2():
    json_from_file = open("/Users/Hila/PycharmProjects/SaltAssignment-Hila/test/Json.json", "r")
    schema_from_file = open("/Users/Hila/PycharmProjects/SaltAssignment-Hila/test/Models.json", "r")
    schema_handler = SchemaHandler()
    schema_handler.update_schema(schema_from_file.read())
    assert JsonValidator.validate_json(json_from_file.read(), schema_handler)


