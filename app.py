from flask import Flask, redirect, render_template, json, jsonify, sessions, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, SignupForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import dotenv
import string
import secrets
import psycopg2
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from urllib.parse import urlencode
from models import db, APIKey, UsageLog, Developer
import os
from functools import wraps

load_dotenv()

AUTH0_CLIENT_ID = "fl8SAQwImvtEaHs4068LfYpI2hfNAHTK"
AUTH0_DOMAIN = "dev-2cippwjdymebmpv1.us.auth0.com"
AUTH0_CLIENT_SECRET  = "lSkleCikoqhFXkliEHZsg6K9FebUIVFTDKz4gKnh6ReehwBlaRe0K2IxkaQt_CkR"
AUTH0_CALLBACK_URL="https://vera-jf5t.onrender.com/callback"
APP_URL = "https://vera-jf5t.onrender.com"

app = Flask(__name__)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    uid = int(user_id)
    return Developer.query.get(uid)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    #'postgresql://postgres:ryoiki_tenkai__nehan_no_roka@db.ivajdrrrjktuarovumbd.supabase.co:5432/postgres',
    'postgresql://postgres.ivajdrrrjktuarovumbd:ryoiki_tenkai__nehan_no_roka@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres' # Default to SQLite for easy setup
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("r62K`ERW4n5dpybz<()eR~](&uQ=f)`yjtFXwNET{>8R?7GQXKtKG$<)Mt>h$$6")
app.config["SECRET_KEY"] = "r62K`ERW4n5dpybz<()eR~](&uQ=f)`yjtFXwNET{>8R?7GQXKtKG$<)Mt>h$$6"

oauth = OAuth(app)
'''auth0 = oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    api_base_url=f"https://{os.environ.get('AUTH0_DOMAIN')}",
    access_token_url=f"https://{os.environ.get('AUTH0_DOMAIN')}/oauth/token",
    authorize_url=f"https://{os.environ.get('AUTH0_DOMAIN')}/authorize",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{os.environ.get('AUTH0_DOMAIN')}/.well-known/openid-configuration"
)'''

auth0 = oauth.register(
    "VERA",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=f"https://{AUTH0_DOMAIN}",
    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",
    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration"
)


db.init_app(app)

'''@app.cli.command('init-db')
def init_db():
    #db.init_app(app)
    """Create all database tables."""
    with app.app_context():
        # Drop all tables and then create them (DANGEROUS: use for development only)
        # db.drop_all() 
        db.create_all()
        print("Database tables created!")'''


def get_app_url():
    return os.environ.get("APP_URL", "https://vera-jf5t.onrender.com")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login_google")
def login_google():
    try:
        app_url = get_app_url()
        return auth0.authorize_redirect(
            redirect_uri=f"{app_url}/callback",
            connection="google-oauth2" 
        )
    except Exception as ex:
        return {"error":ex}


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    signup_form = SignupForm()
    
    if request.method == 'POST':
        # We check which form is being validated/submitted
        
        # 1. Login Form Logic
        if request.form.get('login_submit') and login_form.validate_on_submit():
            # Process login_form.email.data and login_form.password.data
            user = Developer.query.filter_by(email = login_form.email.data).first()
            if user:
                if check_password_hash(user.auth0_user_id, login_form.password.data):
                    login_user(user, remember = login_form.data)
                    return redirect(url_for("dashboard"))
            
        # 2. Signup Form Logic
        if request.form.get('signup_submit') and signup_form.validate_on_submit():
            # Process signup_form.name.data, signup_form.email.data, etc.
            if signup_form.validate_on_submit():
                hashed_password = generate_password_hash(signup_form.password.data)
                new_user = Developer(
                    name = signup_form.name.data,
                    email = signup_form.email.data,
                    auth0_user_id = hashed_password
                )
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for("login"))
        
        # Fall through if validation fails for either submitted form

    return render_template('login.html', 
                           login_form=login_form, 
                           signup_form=signup_form)
    

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user = current_user)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user = current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/api_key", methods=["POST"])
def create_api_key():
    key_exists = APIKey.query.filter_by(developer_id = current_user.developer_id, is_active = True).first()
    if key_exists:
        key_exists.is_active = False
    key = secrets.token_urlsafe(32)
    new_apikey = APIKey(
        developer_id = current_user.developer_id,
        api_key_hash = generate_password_hash(key),
        key_prefix = secrets.token_urlsafe(16)
    )
    db.session.add(new_apikey)

    db.session.commit()
    return jsonify({
        "api_key":key
    })

@app.route("/callback")
def callback():
    try:
        # 1. Exchange the code for the token
        token = auth0.authorize_access_token()
        
        # 2. Get user info directly from the token (saves a network call)
        userinfo = token.get("userinfo")
        if not userinfo:
            # Fallback if userinfo isn't in the token
            userinfo = auth0.get("userinfo").json()

        aui = userinfo["sub"]
        email = userinfo.get("email", "")
        name = userinfo.get("name", "")

        # 3. DB Logic
        user = Developer.query.filter_by(auth0_user_id=aui).first()
        
        if not user:
            user = Developer(
                name=name,
                email=email,
                auth0_user_id=aui
            )
            db.session.add(user)
            db.session.commit()

        # 4. Flask-Login session creation
        login_user(user, remember=True)
        return redirect(url_for("dashboard"))

    except Exception as e:
        app.logger.error(f"Login callback error: {e}")
        flash("Login failed. Please try again.", "danger")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)