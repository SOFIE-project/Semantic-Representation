import os
import yaml

class Config(object):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'static/config.yaml')
    with open(CONFIG_PATH, 'r') as config_yaml:                         
        config = yaml.load(config_yaml, Loader=yaml.FullLoader)

    SECRET_KEY = os.environ.get('SECRET_KEY') or config['secret_key']
    HOST = config['host']
    PORT = config['port']
    DEBUG = config['debug']   
