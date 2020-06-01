from project.api import bp


@bp.route('/api/v1/validate', methods=['POST'])
def validate_task():
    if not request.json:
        return flask.make_response(flask.jsonify({'status': 'error', 'message': 'json file missing'}), 400)
    validation_results = validate_semantic(request.json)
    if validation_results is True:
        return flask.jsonify({'status': 'success', 'data': 'null'})
    else:
        return flask.make_response(flask.jsonify({'status': 'fail', 'data': validation_results}), 400)


@bp.route('/api/v1/getschema', methods=['GET'])
def get_iot_schema():
    return flask.jsonify(app.custom_schema)