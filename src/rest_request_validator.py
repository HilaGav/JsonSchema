import json
from src.schema_handler import SchemaHandler
from src.types_handler import TypesHandler
from src.utils import to_dictionary


class RestRequestValidator:
    __schema_handler = None
    __type_handler = None

    def __init__(self, schema_handler: SchemaHandler, type_handler: TypesHandler):
        self.__schema_handler = schema_handler
        self.__type_handler = type_handler

    def validate_json(self, jsons_to_validate):
        json_datas = json.loads(jsons_to_validate)
        return self.__deep_validate(json_datas)

    def __deep_validate(self, rest_requests):
        reason_of_fail = {}
        schema_structures_type = self.__schema_handler.schemaStructuresType
        schema_structures_required = self.__schema_handler.schemaStructuresRequired

        for rest_request in rest_requests:
            schema = self.__schema_handler.get_schema(rest_request.get('method'), rest_request.get('path'))

            for schema_structure in schema_structures_type:
                type_valid = self.__validate_type(schema.get(schema_structure), rest_request.get(schema_structure))
                if len(type_valid) > 0:
                    reason_of_fail.update({"Types error": type_valid})

            for schema_structure in schema_structures_required:
                required_valid = self.__validate_required_field(schema.get(schema_structure.get('required')),
                                                                rest_request.get(schema_structure.get('name')))
                if len(required_valid) > 0:
                    reason_of_fail.update({"Required field errors": required_valid})

        return reason_of_fail

    @staticmethod
    def __validate_required_field(required_field, rest_request):
        reason_of_fail = {}
        if required_field is not None and len(required_field) != 0:
            name_to_rest_request = to_dictionary(rest_request, 'name')
            for required in required_field:
                if not name_to_rest_request.get(required.get('name')):
                    reason_of_fail.update({"error": f"Cant find required field:{required}"})

        return reason_of_fail

    def __validate_type(self, fields_schema, rest_request):
        reason_of_fail = {}
        if rest_request is not None:
            for field in rest_request:
                field_schema = fields_schema.get(field.get('name'))
                if not field_schema:
                    reason_of_fail.update({"error": "Field not exist in schema"})

                types = field_schema.get("types")
                value = field.get('value')

                is_find_type = False
                for type in types:
                    if self.__type_handler.validate_type(type, value):
                        is_find_type = True
                if not is_find_type:
                    reason_of_fail.update({"error": f"Cant find match type to field:{field}"})

        return reason_of_fail
