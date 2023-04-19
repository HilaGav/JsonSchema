import json


class SchemaHandler:
    def __init__(self):
        self.MethodAndPathToValue = {}

    """
            indexing method+path to find the appropriate schema without iterating over the array of schemas.
            indexing field 'name' in query_params, headers, body
            I decided not to indexing type to not slow down the insert too much
    """
    def update_schema(self, schemas_json):
        schemas = json.loads(schemas_json)
        self.MethodAndPathToValue = {}

        for schema in schemas:
            key = schema.get('method') + schema.get('path')
            query_params_by_name = self.__convert_list_to_dic_by_field(schema.get('query_params'), 'name')
            headers_by_name = self.__convert_list_to_dic_by_field(schema.get('headers'), 'name')
            body_by_name = self.__convert_list_to_dic_by_field(schema.get('body'), 'name')

            self.MethodAndPathToValue.update({key: {
                                                    "query_params": query_params_by_name,
                                                    "headers": headers_by_name,
                                                    "body": body_by_name
                                                    }})

    def get_schema_by_method_and_path(self, method: str, path: str):
        return self.MethodAndPathToValue[method + path]

    @staticmethod
    def __convert_list_to_dic_by_field(list: list, field: str):
        new_dict = {}
        for item in list:
            name = item.pop(field)
            new_dict[name] = item
        return new_dict