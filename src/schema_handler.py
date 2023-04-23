import json
from src.utils import to_dictionary


class SchemaHandler:
    def __init__(self):
        self.EndPointsToValue = {}
        self.schemaStructuresType = ['headers', 'query_params', 'body']
        self.schemaStructuresRequired = [{'required': 'query_params_required', 'name': 'query_params'},
                                         {'required': 'headers_required', 'name': 'headers'},
                                         {'required': 'body_required', 'name': 'body'}]

    """
            indexing method+path to find match schema without iterating over the array of schemas.
            indexing field 'name' in query_params, headers, body
            I decided not to indexing type to not slow down the insert too much
    """
    def update_schema(self, schemas_json):
        schemas = json.loads(schemas_json)

        if schemas is None:
            return False

        new_end_points_to_value = {}
        for schema in schemas:
            method, path = schema.get('method'), schema.get('path')
            if method is None or path is None:
                return False

            endpoint = method + path
            query_params, headers, body = schema.get('query_params'), schema.get('headers'), schema.get('body')

            query_params_required = self.get_required_fields(query_params)
            headers_required = self.get_required_fields(headers)
            body_required = self.get_required_fields(body)

            query_params_by_name = to_dictionary(query_params, 'name')
            headers_by_name = to_dictionary(headers, 'name')
            body_by_name = to_dictionary(body, 'name')

            new_end_points_to_value.update({
                endpoint: {
                    "query_params_required": query_params_required,
                    "headers_required": headers_required,
                    "body_required": body_required,
                    "query_params": query_params_by_name,
                    "headers": headers_by_name,
                    "body": body_by_name
                }})

        self.EndPointsToValue = new_end_points_to_value
        return True

    @staticmethod
    def get_required_fields(parameters):
        return [query_param for query_param in parameters if query_param.get('required')]

    def get_schema(self, method: str, path: str):
        return self.EndPointsToValue.get(method + path)
