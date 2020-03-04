from flask import Flask
from .config import Config
from .manage_schema import ManageSchema

import os
import sys

app = Flask(__name__)
# Add default configuration to app
app.config.from_object(Config)

# Add schemas to app
try:
    manageSchema = ManageSchema(app.config['SCHEMA_PATH'])
except FileNotFoundError as err:
    print(err)
    print("Mandatory files missing")
    sys.exit(os.EX_SOFTWARE)

app.custom_schema = manageSchema.get_custom_schema_json()

from project import routes
