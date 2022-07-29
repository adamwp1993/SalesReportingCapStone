from flask import Flask, request, render_template, jsonify, redirect, session, url_for, flash
from datetime import timedelta
import callAPI
import params
import hashlib
from model import Model
from database import Database
import secrets

app = Flask(__name__)
app.static_folder = 'static'

# Set the app secret key for login sessions

# secret = secrets.token_urlsafe(32)
# app.secret_key = secret


# Build ML model so we can call it later
model = Model()
# Build database
database = Database()
# Set Session timeout - default 20 minutes
# session.permanent = True
# app.permanent_session_lifetime = timedelta(minutes=20)

# sessions = {}

# TODO - more stringent input validation
# TODO - each user gets their own unique salt value (possibly the user id?)
# TODO - create new user accounts page

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


# TODO - Build login page
# TODO - loging page POST to server for login

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        valid = database.login(username, password)
        if valid:
            #flash("Authenticated")
            return redirect(url_for('reports'))
    return render_template('home.html')


@app.route('/reports',  methods=['GET', 'POST'])
# Display the reports on the report page
def reports():
    if request.method == 'GET':
        auth_token = callAPI.get_auth_token(params.client_secret, params.client_id, params.login_url)
        embed_url = callAPI.get_embed_url(auth_token, params.workspace_id, params.test_report_id)
        embed_token = callAPI.get_embed_token(auth_token, params.workspace_id, params.test_report_id)
        data = {'embed_url': str(embed_url), 'embed_token': str(embed_token), 'report_id': str(params.test_report_id) }

        return render_template('reports.html', data=data)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    valid = input_validation(data)
    if not valid:
        return "Invalid input"
    result = model.predict(data)

    # Handle request
    return "Predicted Sales: " + str(result[0]) + "<br> Model Accuracy/Variance: " + str(result[1])




