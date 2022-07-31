import os
from flask import Flask, request, render_template, jsonify, redirect, session, url_for, flash, make_response
from datetime import timedelta
import callAPI
import params
from model import Model
from database import Database
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import secrets
from logger import Logger
from user import User

# Initialize web server and set static path for resources
app = Flask(__name__)
app.static_folder = 'static'
# bind flask-login to web server
login_man = LoginManager()
login_man.init_app(app)
# set default login url
login_man.login_view = 'login'
# users list holds logged in users
users = []
log_manager = Logger()
log_manager.write_log("Flask WebServer Started")

@login_man.user_loader
def load_user(user_id):
    for user in users:
        if user.user_id == user_id:
            return user


# Set the app secret key for login sessions

secret = secrets.token_urlsafe(32)
app.secret_key = secret




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




@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    valid = False
    if request.method == 'POST':
        data = request.get_json()
        username = data['user_name']
        password = data['password']
        # Validate Password and username
        if len(username) > 0 and len(password) > 0:
            valid = database.login(username, password)
        # login the user and redirect
        if valid:
            log_manager.write_log(username + " Authenticated")
            user_id = database.get_id(username)
            user = User(username, user_id)
            login_user(user)
            users.append(user)

            res = make_response("Authenticated")
            res.headers['Content-Type'] = 'text/plain'
            res.status_code = 200
            return res
        else:
            res = make_response("Invalid Credentials")
            res.headers['Content-Type'] = 'text/plain'
            res.status_code = 403
            return res

    return render_template('home.html')

@app.route('/logout', methods=['POST'])
def logout():
    current_username = current_user.username
    current_user_id = current_user.user_id
    if current_user.is_authenticated:
        # logout user and remove from the list of authenticated users
        for user in users:
            if user.user_id == current_user_id:
                users.remove(user)
        logout_user()
        log_manager.write_log(current_username + " Logged out")
        res = make_response(current_username + " logged out")
        res.headers['Content-Type'] = 'text/plain'
        res.status_code = 200
        return res


@app.route('/reports',  methods=['GET', 'POST'])
@login_required
# Display the reports on the report page
def reports():

    auth_token = callAPI.get_auth_token(params.client_secret, params.client_id, params.login_url)
    embed_url = callAPI.get_embed_url(auth_token, params.workspace_id, params.report_id)
    embed_token = callAPI.get_embed_token(auth_token, params.workspace_id, params.report_id)
    data = {'embed_url': str(embed_url), 'embed_token': str(embed_token), 'report_id': str(params.report_id)}
    log_manager.write_log("Authentication and embed token retrieved from PowerBI API")
    return render_template('reports.html', data=data)


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.get_json()
    valid = input_validation(data)
    if not valid:
        return "Invalid input"
    result = model.predict(data)
    log_manager.write_log("Prediction input:\n" + str(data))
    log_manager.write_log("Prediction: " + str(result[0]))


    # Handle request
    return "Predicted Sales: " + str(result[0]) + "<br> Model Accuracy/Variance: " + str(result[1])

app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

