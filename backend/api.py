from flask import Flask
from flask import request
from run import generate_thing
from flask_cors import CORS
from flask import send_file

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def hello_world():
    generate_thing(request.json.get('gauges'), request.json.get('log'))
    return send_file('test.mp4')
    # return "<p>Hello, World!</p>"