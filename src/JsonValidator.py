import json
from src.utils import convert_list_to_dictionary_by_field


class JsonValidator:
    @staticmethod
    def validate_json(json_data, schema_handler):
        json_datas = json.loads(json_data)

        return JsonValidator.__validate(json_datas, schema_handler)

    @staticmethod
    def __validate(json_datas, schema_handler):
        is_valid = False
        for json_data in json_datas:
            schema = schema_handler.get_schema_by_method_and_path(json_data.get('method'), json_data.get('path'))
            if not (JsonValidator.__validate_type(schema.get('headers'), json_data.get('headers')) and
                    JsonValidator.__validate_type(schema.get('query_params'), json_data.get('query_params')) and
                    JsonValidator.__validate_type(schema.get('body'), json_data.get('body'))):
                return False
            if not (JsonValidator.__validate_required_field(schema.get('query_params_required'),
                                                            json_data.get('query_params')) and
                    JsonValidator.__validate_required_field(schema.get('headers_required'), json_data.get('headers'))
                    and JsonValidator.__validate_required_field(schema.get('body_required'), json_data.get('body'))):
                return False

            else:
                is_valid = True

        return is_valid

    @staticmethod
    def __validate_required_field(required_field, json_data):
        name_to_json_data = convert_list_to_dictionary_by_field(json_data, 'name')
        for required in required_field:
            if not name_to_json_data.get(required):
                return False

        return True

    @staticmethod
    def __validate_type(all_field_schema, json_data):
        for field in json_data:
            field_schema = all_field_schema.get(field.get('name'))
            if not field_schema:
                return False
            types = field_schema.get("types")
            value = field.get('value')

            for type in types:
                if type == "String":
                    if not isinstance(value, str):
                        return False
                elif type == "Int":
                    if not isinstance(value, (int)):
                        return False
                elif type == "Boolean":
                    if not isinstance(value, bool):
                        return False
                elif type == "null":
                    if value is not None:
                        return False
                else:
                    return False
        return True
