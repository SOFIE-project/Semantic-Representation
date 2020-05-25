import jsonschema
from project.models import User, TDSchema
from project import db


class ManageSchema(object):

    def __init__(self):
        pass

    def get_schema(self, schema_name):
        raise NotImplementedError

    def update_schema(self, schema_name, schema, username):
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

    def update_schema(self, schema_name, new_schema, username):
        if not valid_schema(new_schema):
            raise jsonschema.exceptions.SchemaError
        if not update_permission(username):
            raise PermissionError
        old_schema = TDSchema.query.filter_by(schema_name=schema_name).first()
        if old_schema is None:
            raise FileNotFoundError()
        old_schema.schema = new_schema
        db.session.commit()


def update_permission(username):
    raise NotImplementedError


def valid_schema(schema):
    raise NotImplementedError


class JsonValidatorImp(JsonValidator):

    def __init__(self, manage_schema):
        if not isinstance(manage_schema, ManageSchema):
            raise ValueError
        super().__init__()
        self.manage_schema = manage_schema

    def validate_msg(self, msg, schema_name):
        schema = self.manage_schema.get_schema(schema_name)
        jsonschema.validate(instance=msg, schema=schema)
