import datetime
import uuid
import src.config as config
import re
import json


class TypesHandler:
    def __init__(self):
        self.Types = {"String": self.is_string,
                      "Int": self.is_int,
                      "Boolean": self.is_bool,
                      "null": self.is_null,
                      "Date": self.is_date,
                      "Email": self.is_email,
                      "UUID": self.is_UUID,
                      "Auth-Token": self.is_auth_token,
                      "List": self.is_list}

        self.TypesPrimitive = ["String", "Int", "Boolean", "List"]

    def type_validate(self, type, value):
        type_function = self.Types.get(type)
        if type_function is not None:
            return type_function(value)
        return False

    def type_validate_primitive(self, value):
        for type_primitive in self.TypesPrimitive:
            if self.type_validate(type_primitive, value):
                return True
        if self.is_object(value):
            return True
        return False

    @staticmethod
    def is_string(value):
        return isinstance(value, str)

    @staticmethod
    def is_int(value):
        return isinstance(value, int)

    @staticmethod
    def is_bool(value):
        return isinstance(value, bool)

    @staticmethod
    def is_null(value):
        if value is not None:
            return False

    @staticmethod
    def is_date(value):
        if not isinstance(value, str):
            return False
        try:
            datetime.datetime.strptime(value, config.valid_date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_email(email):
        return re.match(config.email_regex, str(email)) is not None

    @staticmethod
    def is_UUID(uuid_str):
        try:
            uuid.UUID(str(uuid_str))
            return True
        except ValueError:
            return False

    @staticmethod
    def is_auth_token(auto_token):
        return re.match(config.bearer_regex, str(auto_token)) is not None

    @staticmethod
    def is_object(object_json):
        if object_json is not None:
            if json.dumps(object_json) is not None:
                return True
        return False

    def is_list(self, list_fields):
        if not isinstance(list_fields, list):
            return False
        if list_fields is None or len(list_fields) <= 0:
            return False
        for field in list_fields:
            if not self.type_validate_primitive(field):
                return False
        return True
