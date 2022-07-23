from flask import Flask, request, render_template, jsonify
import callAPI
import params
from model import Model

app = Flask(__name__)
app.static_folder = 'static'

#Build ML model so we can call it later
model = Model()

# Routing or Mapping - tie a URL to a python webpage
# TODO - https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript
# TODO - https://www.freecodecamp.org/news/jquery-ajax-post-method/


def input_validation(data):
    # return true if input is good
    try:
        store = int(data['storeNum'])
        temp = int(data['temp'])
        cpi = float(data['cpi'])
        gasPrice = float(data['gasPrice'])
    except ValueError:
        return False

    if 45 < store < 1:
        return False
    if 500 < cpi < 0:
        return False
    else:
        return True




@app.route('/')
def home():
    return "<h1>Hello World!<h1>\n" \
           "Method Used to get this page: %s" % request.method


@app.route('/reports',  methods=['GET', 'POST'])
# Display the reports on the report page
def embed():
    auth_token = callAPI.get_auth_token(params.client_secret, params.client_id, params.login_url)
    embed_url = callAPI.get_embed_url(auth_token, params.workspace_id, params.test_report_id)
    embed_token = callAPI.get_embed_token(auth_token, params.workspace_id, params.test_report_id)
    data = { 'embed_url': str(embed_url), 'embed_token': str(embed_token), 'report_id': str(params.test_report_id) }

    return render_template('reports.html', data=data)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    valid = input_validation(data)
    if not valid:
        return "Invalid input"
    result = model.predict(data)

    # Handle request
    return str(result)



#app.run(debug=True)

