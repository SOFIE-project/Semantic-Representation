from app import app
import flask
import json
import yaml
import os
from .semantic_json_validator import validate_semantic
from flask import request, jsonify, render_template

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# REST API for validate JSON object
@app.route('/api/v1/validate', methods=['POST'])
def validate_task():
    if not request.json:
        flask.abort(400) #TODO more informative message
    return 201 if validate_semantic(request.json) else flask.abort(flask.Response('Validation failed'))

@app.route('/api/v1/getschema', methods=['GET'])
def get_schema():
    basedir = os.path.abspath(os.path.dirname(__file__))
    schema_path = os.path.join(basedir, app.config['schema_path'])
    try:
        with open(schema_path, 'r') as json_file:
            schema = json.load(json_file)
    except FileNotFoundError:
        return render_template('error_schema.html') #TODO add return error code
    return render_template('schema.html', schema=schema)

