import jsonschema
import json
from project.models import User, TDSchema
from app import db

ADD_SCHEMA = 'add_schema'
REMOVE_SCHEMA = 'remove_schema'


class ManageSchema(object):

    def __init__(self):
        pass

    def get_schema(self, schema_name):
        raise NotImplementedError

    def add_schema(self, schema):
        raise NotImplementedError

    def update_schema(self, schema_name, schema):
        raise NotImplementedError

    def remove_schema(self, schema_name):
        raise NotImplementedError


class JsonValidator(object):

    def __init__(self):
        pass

    def validate_msg(self, msg, schema_name):
        raise NotImplementedError


class ManageSchemaImp(ManageSchema):

    def __init__(self):
        super().__init__()

    # ToDo consider a function that keeps the schema in memory instead of calling always the db
    def get_schema(self, schema_name):
        schema = TDSchema.query.filter_by(schema_name=schema_name).first()
        if schema is None:
            raise FileNotFoundError()
        return schema.schema

    def add_schema(self, schema):
        if not valid_request(ADD_SCHEMA, schema):
            raise error_handler('Request not valid')
        schema = json.loads(schema)
        name = schema['schema_name']
        td = str(schema['schema'])
        schema = TDSchema.query.filter_by(schema_name=name).first()
        if schema is None:
            query = TDSchema(schema_name=name, schema=td)
            db.session.add(query)
            db.session.commit()
            return message_handler('Schema added correctly')
        return error_handler('Schema already in the db')

    def update_schema(self, schema_name, new_schema):
        if not valid_schema(new_schema):
            raise jsonschema.exceptions.SchemaError
        old_schema = TDSchema.query.filter_by(schema_name=schema_name).first()
        if old_schema is None:
            raise FileNotFoundError()
        old_schema.schema = new_schema
        db.session.commit()

    def remove_schema(self, schema_name):
        if not valid_request(REMOVE_SCHEMA, schema_name):
            raise error_handler('Request not valid')
        schema = TDSchema.query.filter_by(schema_name=schema_name).first()
        if schema is None:
            return error_handler('Schema not found')
        db.session.remove(schema)
        db.sessio.commit()
        return message_handler('Schema removed correctly')


class JsonValidatorImp(JsonValidator):

    def __init__(self):
        super().__init__()

    def validate_msg(self, msg, schema):
        jsonschema.validate(instance=msg, schema=schema)


def message_handler(message):
    if not isinstance(message, str):
        raise ValueError
    return json.dumps({'data': message}), 200


def error_handler(message):
    if not isinstance(message, str):
        raise ValueError
    return json.dumps({'error': message}), 500


def valid_request(type, message):
    if type == ADD_SCHEMA:
        schema = {'schema_name': 'string', 'schema': 'string'}
        instance = message
    elif type == REMOVE_SCHEMA:
        schema = {'schema_name': 'string'}
        instance = message
    else:
        return False
    jsonschema.validate(instance, schema)
    return True


def update_permission(username):
    raise NotImplementedError


def valid_schema(schema):
    raise NotImplementedError