import json
from src.utils import convert_list_to_dictionary_by_field


class SchemaHandler:
    def __init__(self):
        self.EndPointsToValue = {}

    """
            indexing method+path to find the appropriate schema without iterating over the array of schemas.
            indexing field 'name' in query_params, headers, body
            I decided not to indexing type to not slow down the insert too much
    """
    def update_schema(self, schemas_json):
        schemas = json.loads(schemas_json)
        self.EndPointsToValue = {}

        for schema in schemas:
            key = schema.get('method') + schema.get('path')
            query_params_required = [query_param for query_param in schema.get('query_params') if
                                     query_param.get('required')]
            headers_required = [query_param for query_param in schema.get('headers') if query_param.get('required')]
            body_required = [query_param for query_param in schema.get('body') if query_param.get('required')]

            query_params_by_name = convert_list_to_dictionary_by_field(schema.get('query_params'), 'name')
            headers_by_name = convert_list_to_dictionary_by_field(schema.get('headers'), 'name')
            body_by_name = convert_list_to_dictionary_by_field(schema.get('body'), 'name')

            self.EndPointsToValue.update({key: {
                "query_params_required": query_params_required,
                "headers_required": headers_required,
                "body_required": body_required,
                "query_params": query_params_by_name,
                "headers": headers_by_name,
                "body": body_by_name
            }})

    def get_schema_by_method_and_path(self, method: str, path: str):
        return self.EndPointsToValue[method + path]
