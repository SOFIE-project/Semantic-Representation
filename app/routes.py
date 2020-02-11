from app import app
import flask
from .semantic_validator import validate_semantic
from flask import request, jsonify, render_template



# Test rutes
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# REST API for validate JSON object
@app.route('/api/v1/validate', methods=['POST'])
def validate_task():
    if not request.json:
        flask.abort(400) #TODO more informative message
    return 201 if validate_semantic(request.json) else flask.abort(flask.Response('Validation failed'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)