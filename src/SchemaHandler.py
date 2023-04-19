import json


class SchemaHandler:
    def __init__(self):
        self.MethodAndPathToValue = {}

    def update_schema(self, schemas_json):
        schemas = json.loads(schemas_json)
        self.MethodAndPathToValue = {}
        for schema in schemas:
            self.MethodAndPathToValue.update({schema.get('method') + schema.get('path'):
                                             {"query_params": schema.get('query_params'),
                                             "headers": schema.get('headers'), "body": schema.get('body')}})

    def get_schema_by_method_and_path(self, method, path):
        return self.MethodAndPathToValue[method + path]