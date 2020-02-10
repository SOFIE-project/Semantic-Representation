import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)