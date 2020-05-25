from project import app
import flask
from .semantic_json_validator import validate_semantic
from flask import request


@app.route('/api/v1/register', methods=['POST'])
def register():
    pass


@app.route('/api/v1/add_schema', methods=['POST'])
def add_schema():
    pass


@app.route('/api/v1/update_schema', methods=['POST'])
def update_schema():
    pass


# REST API for validate JSON object
@app.route('/api/v1/validate', methods=['POST'])
def validate_task():
    if not request.json:
        return flask.make_response(flask.jsonify({'status': 'error', 'message': 'json file missing'}), 400)
    validation_results = validate_semantic(request.json)
    if validation_results is True:
        return flask.jsonify({'status': 'success', 'data': 'null'})
    else:
        return flask.make_response(flask.jsonify({'status': 'fail', 'data': validation_results}), 400)


@app.route('/api/v1/getschema', methods=['GET'])
def get_iot_schema():
    return flask.jsonify(app.custom_schema)


