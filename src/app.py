from flask import Flask, request, Response
from src.schema_handler import SchemaHandler
from src.json_validator import JsonValidator
from src.types_handler import TypesHandler

app = Flask(__name__)

schema_handler = SchemaHandler()
type_handler = TypesHandler()
json_validate = JsonValidator(schema_handler, type_handler)


@app.route('/LearnedModel/Update', methods=['PUT'])
def update_learn_model():
    learn_model = request.get_data()
    if schema_handler.update_schema(learn_model):
        return Response("update model", status=200)

    return Response("not update model", status=400)


@app.route('/Validate/RestApi', methods=['POST'])
def validate_rest_api():
    if not schema_handler.EndPointsToValue:
        return Response("Did not find learned model", status=400)

    json_to_check = request.get_data()
    if json_validate.validate_json(json_to_check):
        return Response("Valid!", status=200)

    return Response("Not valid", status=400)


app.run()
