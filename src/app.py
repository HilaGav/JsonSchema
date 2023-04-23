import json

from flask import Flask, request, Response
from src.schema_handler import SchemaHandler
from src.rest_request_validator import RestRequestValidator
from src.types_handler import TypesHandler

app = Flask(__name__)

schema_handler = SchemaHandler()
type_handler = TypesHandler()
json_validate = RestRequestValidator(schema_handler, type_handler)


@app.route('/LearnedModel/Update', methods=['PUT'])
def update_learn_model():
    learn_model = request.get_data()
    if schema_handler.update_schema(learn_model):
        return Response("update model", status=200)

    return Response("not update model", status=400)


@app.route('/Validate/RestApi', methods=['POST'])
def validate_rest_api():
    if not schema_handler.EndPointsToValue:
        return Response("Did not find learned model", status=404)

    json_to_check = request.get_data()
    reason_of_failed = json_validate.validate_json(json_to_check)
    if len(reason_of_failed) == 0:
        return Response("Valid!", status=200)

    return Response(json.dumps(reason_of_failed), status=400)


app.run()
