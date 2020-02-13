from project import app
import os
import yaml
import project.tests.test_basic

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])