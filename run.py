from config import Config
from project import create_app

config = Config()
app = create_app(config)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
