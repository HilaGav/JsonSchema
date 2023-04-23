import json
from src.schema_handler import SchemaHandler
from src.types_handler import TypesHandler
from src.utils import convert_list_to_dictionary_by_field


class JsonValidator:
    __schema_handler = None
    __type_handler = None

    def __init__(self, schema_handler: SchemaHandler, type_handler: TypesHandler):
        self.__schema_handler = schema_handler
        self.__type_handler = type_handler

    def validate_json(self, jsons_to_validate):
        json_datas = json.loads(jsons_to_validate)
        return self.__deep_validate(json_datas)

    def __deep_validate(self, json_datas):
        reason_of_fail = {}
        schema_structures_type = self.__schema_handler.schemaStructuresType
        schema_structures_required = self.__schema_handler.schemaStructuresRequired

        for json_data in json_datas:
            schema = self.__schema_handler.get_schema_by_method_and_path(json_data.get('method'), json_data.get('path'))

            for schema_structure in schema_structures_type:
                type_valid = self.__validate_type(schema.get(schema_structure), json_data.get(schema_structure))
                if len(type_valid) > 0:
                    reason_of_fail.update({"Type error": type_valid})

            for schema_structure in schema_structures_required:
                required_valid = self.__validate_required_field(schema.get(schema_structure.get('required')),
                                                                json_data.get(schema_structure.get('name')))
                if len(required_valid) > 0:
                    reason_of_fail.update({"Required field errors": required_valid})

        return reason_of_fail

    @staticmethod
    def __validate_required_field(required_field, json_data):
        reason_of_fail = {}
        if required_field is not None and len(required_field) is not 0:
            name_to_json_data = convert_list_to_dictionary_by_field(json_data, 'name')
            for required in required_field:
                if not name_to_json_data.get(required.get('name')):
                    reason_of_fail.update({"error": f"Cant find required field:{required}"})

        return reason_of_fail

    def __validate_type(self, all_field_schema, json_data):
        reason_of_fail = {}
        if json_data is not None:
            for field in json_data:
                field_schema = all_field_schema.get(field.get('name'))
                if not field_schema:
                    reason_of_fail.update({"error": "Field not exist in schema"})
                    break

                types = field_schema.get("types")
                value = field.get('value')

                is_find_type = False
                for type in types:
                    if self.__type_handler.type_validate(type, value):
                        is_find_type = True
                if not is_find_type:
                    reason_of_fail.update({"error": f"Cant find match type to field:{field}"})

        return reason_of_fail
