from flask import Flask, request, render_template
import callAPI
import params

app = Flask(__name__)
app.static_folder = 'static'
# Routing or Mapping - tie a URL to a python webpage
# TODO - https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript


@app.route('/')
def home():
    return "<h1>Hello World!<h1>\n" \
           "Method Used to get this page: %s" % request.method


@app.route('/test')
def test():
    return "<h1>testing routes</h1>"


@app.route('/reports')
# Display the reports on the report page
def embed():
    auth_token = callAPI.get_auth_token(params.client_secret, params.client_id, params.login_url)
    embed_url = callAPI.get_embed_url(auth_token, params.workspace_id, params.test_report_id)
    embed_token = callAPI.get_embed_token(auth_token, params.workspace_id, params.test_report_id)
    data = { 'embed_url': str(embed_url), 'embed_token': str(embed_token), 'report_id': str(params.test_report_id) }

    return render_template('reports.html', data=data)


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

# HTML templates return .templates pages

app.run(debug=True)

