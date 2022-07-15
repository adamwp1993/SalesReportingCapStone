from flask import Flask, request

app = Flask(__name__)

# Routing or Mapping - tie a URL to a python webpage


@app.route('/')
def home():
    return "<h1>Hello World!<h1>\n" \
           "Method Used to get this page: %s" % request.method

@app.route('/test')
def test():
    return "<h1>testing routes</h1>"

# if you want to put variable in URL use angle brackets
@app.route('/hello/<user>')
def hello(user):
    return "<h1>Hello %s</h1>" % user

# HTTP methods and handling different HTTP types
@app.route('/postme', methods=['GET', 'POST'])
def postme():
    if request.method == 'POST':
        return "Nioce post request!"
    else:
        return "try posting me next time!"

app.run(debug=True)

