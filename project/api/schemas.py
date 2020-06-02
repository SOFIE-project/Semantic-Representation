from project import db
from project.api import bp
from project.api.errors import bad_request
from flask import request, jsonify
from project.models import Schema


@bp.route('/add_schema', methods=['POST'])
def add_schema():
    data = request.get_json() or {}
    if 'name' not in data or 'schema' not in data:
        return bad_request('must include schema and schema name')
    if Schema.query.filter_by(name=data['name']).first():
        return bad_request('schema name already saved')
    schema = Schema()
    schema.from_dict(data)
    db.session.add(schema)
    db.session.commit()
    response = jsonify(schema.to_dict())
    response.status_code = 200
    return response


@bp.route('/remove_schema', methods=['POST'])
def remove_schema():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include the schema name')
    schema = Schema.query.filter_by(name=data['name']).first()
    if schema is None:
        return bad_request('schema not found')
    db.session.delete(schema)
    db.session.commit()
    response = jsonify({'message': 'schema removed'})
    response.status_code = 200
    return response


@bp.route('/update_schema', methods=['POST'])
def update_schema():
    data = request.get_json() or {}
    if 'name' not in data or 'schema' not in data:
        return bad_request('must include schema and schema name')
    schema = Schema.query.filter_by(name=data['name']).first()
    if schema is None:
        return bad_request('schema not found')

    schema.from_dict(data)
    db.session.commit()
    response = jsonify(schema.to_dict())
    response.status_code = 200
    return response


@bp.route('/extend_schema', methods=['POST'])
def extend_schema():
    pass


@bp.route('/get_schema/<int:id>', methods=['GET'])
def get_schema2(id):
    schema = Schema.query.get_or_404(id)
    return jsonify(schema.schema)


@bp.route('/get_schema', methods=['POST'])
def get_schema():
    data = request.get_json() or {}
    schemas_dict = {}
    if 'name' not in data:
        schemas = Schema.query.all()
        for schema in schemas:
            schemas_dict.update(schema.to_dict())
    else:
        schema = Schema.query.filter_by(name=data['name']).first()
        if schema is None:
            return bad_request('schema not found')
        schemas_dict.update(schema.to_dict())
    response = jsonify(schemas_dict)
    response.status_code = 200
    return response


