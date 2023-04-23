import json
from src.schema_handler import SchemaHandler
from src.types_handler import TypesHandler
from src.utils import convert_list_to_dictionary_by_field


class JsonValidator:
    __schema_handler = None
    __type_handler = None

    #TODO: maybe a class that look like json schema
    def __init__(self, schema_handler: SchemaHandler, type_handler: TypesHandler):
        self.__schema_handler = schema_handler
        self.__type_handler = type_handler

    def validate_json(self, jsons_to_validate):
        json_datas = json.loads(jsons_to_validate)
        return self.__deep_validate(json_datas)

    def __deep_validate(self, json_datas):
        is_valid = False
        reason_of_fail = {}
        for json_data in json_datas:
            schema = self.__schema_handler.get_schema_by_method_and_path(json_data.get('method'), json_data.get('path'))

            if not (self.__validate_type(schema.get('headers'), json_data.get('headers')) and
                    self.__validate_type(schema.get('query_params'), json_data.get('query_params')) and
                    self.__validate_type(schema.get('body'), json_data.get('body'))):
                return False

            if not (self.__validate_required_field(schema.get('query_params_required'), json_data.get('query_params'))
                    and self.__validate_required_field(schema.get('headers_required'), json_data.get('headers'))
                    and self.__validate_required_field(schema.get('body_required'), json_data.get('body'))):
                return False

            else:
                is_valid = True

        return is_valid

    @staticmethod
    def __validate_required_field(required_field, json_data):
        if required_field is not None and len(required_field) is not 0:
            name_to_json_data = convert_list_to_dictionary_by_field(json_data, 'name')
            for required in required_field:
                if not name_to_json_data.get(required.get('name')):
                    return False

        return True

    def __validate_type(self, all_field_schema, json_data):
        for field in json_data:
            field_schema = all_field_schema.get(field.get('name'))
            if not field_schema:
                return False
            types = field_schema.get("types")
            value = field.get('value')

            is_find_type = False
            for type in types:
                if self.__type_handler.type_validate(type, value):
                    is_find_type = True
            if not is_find_type:
                return False

        return True
