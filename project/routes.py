from project import app
import flask
from .semantic_json_validator import validate_semantic
from .manage_schema import get_schema
from flask import request, render_template

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# REST API for validate JSON object
@app.route('/api/v1/validate', methods=['POST'])
def validate_task():
    if not request.json:
        flask.abort(400) #TODO more informative message
    return 201 if validate_semantic(request.json) else flask.abort(flask.Response('Validation failed'))

@app.route('/api/v1/getiotschema', methods=['GET'])
def get_iot_schema():
    try:
        schema = get_schema() # TODO better pattern to do this
    except FileNotFoundError:
        return render_template('error_schema.html') #TODO add return error code
    return render_template('schema.html', schema=schema)

