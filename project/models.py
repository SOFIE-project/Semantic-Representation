from project import db


class Schema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    schema = db.Column(db.String(2048))

    def __repr__(self):
        return '<Schema {}>'.format(self.schema_name)

    def from_dict(self, data):
        for field in ['name', 'schema']:
            if field in data:
                setattr(self, field, str(data[field]))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'schema': self.schema,
        }
        return data
