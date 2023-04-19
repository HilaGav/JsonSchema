import json


class JsonValidator:
    @staticmethod
    def validate_json(json_data, SchemaHandler):
        SchemaHandler = SchemaHandler
        json_datas = json.loads(json_data)

        return JsonValidator.__validate(json_datas, SchemaHandler)

    @staticmethod
    def __validate(json_datas, SchemaHandler):
        is_valid = False
        for json_data in json_datas:
            schema = SchemaHandler.get_schema_by_method_and_path(json_data.get('method'), json_data.get('path'))
            if not (JsonValidator.__validate_type(schema.get('headers'), json_data.get('headers')) and \
                    JsonValidator.__validate_type(schema.get('body'), json_data.get('body'))):
                return False
            else:
                is_valid = True

        return is_valid

    @staticmethod
    def __validate_type(all_field_schema, json_data):
        for field in json_data:
            field_schema = all_field_schema.get(field.get('name'))
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
        return True
