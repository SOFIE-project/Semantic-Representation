import os
import yaml


class Config(object):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'static/config.yaml')
    yaml_config = yaml.load(open(CONFIG_PATH, 'r'), Loader=yaml.FullLoader)

    # Config binding to app variable for separation
    SECRET_KEY = os.environ.get('SECRET_KEY') or yaml_config['secret_key']
    HOST = yaml_config['host']
    PORT = yaml_config['port']
    DEBUG = yaml_config['debug']
    SCHEMA_PATH = yaml_config['schema_path']
    IOT_SCHEMA_PATH = yaml_config['iot_schema_path']
    ERROR_MESSAGES_PATH = yaml_config['error_messages_path']
