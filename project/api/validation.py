from project.api import bp
from project.api.errors import bad_request
from project.models import Schema
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from functools import wraps
import jsonschema
import json
import ast


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest:
            return bad_request("payload must be a valid json")
        return f(*args, **kw)
    return wrapper


@bp.route('/validate', methods=['POST'])
@validate_json
def validate_task():
    data = request.get_json() or {}
    if 'message' not in data or 'schema_name' not in data:
        return bad_request('must include message and schema name')
    schema = Schema.query.filter_by(name=data['schema_name']).first()
    # ToDo error handling
    schema = ast.literal_eval(schema.schema)
    schema = json.loads(json.dumps(schema))
    instance = json.loads(json.dumps(data['message']))
    if schema is None:
        return bad_request('schema not found')
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except (jsonschema.ValidationError, jsonschema.exceptions.SchemaError) as e:
        return bad_request('not valid, ' + e.message)
    response = jsonify({'message': 'valid'})
    response.status_code = 200
    return response



