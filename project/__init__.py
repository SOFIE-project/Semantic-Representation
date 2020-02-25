from flask import Flask
from .config import Config
import os
import yaml

app = Flask(__name__)
# Add default configuration to app
app.config.from_object(Config)

# Add error messages and schema
root_dir = os.path.abspath(os.path.dirname(__file__))
custom_msg_path = os.path.join(root_dir, app.config['ERROR_MSG_PATH'])
schema_path = os.path.join(root_dir, app.config['SCHEMA_PATH'])
app.custom_msg = yaml.load(open(custom_msg_path, 'r'), Loader=yaml.FullLoader)  # ToDo remember the init tests to assure all files are inplace
app.schema = yaml.load(open(schema_path, 'r'), Loader=yaml.FullLoader)

from project import routes
