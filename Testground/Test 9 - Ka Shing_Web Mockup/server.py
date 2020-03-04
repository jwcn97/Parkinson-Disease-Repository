# Imports
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

# Start app
app = Flask(__name__)
# CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})


# Variables
p_var = 0
gp_var = 0

# Home page
@app.route('/')
def function():
	return 'Server check'

# Functions
@app.route('/function1')
@cross_origin()
def function1():
	return 'Function1 working'

@app.route('/function2')
def function2():
	return 'Function2 is also working!'

# Attempt GET
@app.route('/get', methods = ['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get():
	response = jsonify({'some': 'data'})
	# response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# Attempt POST
@app.route('/post', methods = ['POST'])
def request(i):
	global p_var

	p_var += i

@app.route('/postgetwithget', methods = ['GET'])
def request_get():
	return p_var

@app.route('/postgetwithoutget')
def request_get_without_get():
	return p_var

# Attempt GET and POST
@app.route('/', methods = ['GET', 'POST'])
def get_and_post(i):
	global gp_var

	gp_var += i

	return gp_var