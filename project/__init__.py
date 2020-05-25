from flask import Flask
from .config import Config
from .manage_schema import ManageSchema
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import sys

app = Flask(__name__)
# Add default configuration to app
app.config.from_object(Config)


# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Add schemas to app
try:
    manageSchema = ManageSchema(app.config['SCHEMA_PATH'])
except FileNotFoundError as err:
    print(err)
    print("Mandatory files missing")
    sys.exit(os.EX_SOFTWARE)

app.custom_schema = manageSchema.get_custom_schema_json()

from project import routes, models

# Test
'''
user = models.User(username='Admin', password_hash='123')
db.session.add(user)
db.session.commit()
'''


u = models.User.query.get(1)
schema = models.TDSchema(schema_name='test', schema='test', author=u)
db.session.add(schema)
db.session.commit()



