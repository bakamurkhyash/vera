from flask import Flask, redirect, render_template, json, jsonify, sessions, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required
from forms import LoginForm, SignupForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import dotenv
from models import db, APIKey, UsageLog, Developer
import os
from functools import wraps

app = Flask(__name__)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    uid = int(user_id)
    return Developer.query.get(uid)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///vera_dashboard.db' # Default to SQLite for easy setup
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "r62K`ERW4n5dpybz<()eR~](&uQ=f)`yjtFXwNET{>8R?7GQXKtKG$<)Mt>h$$6")
app.config["SECRET_KEY"] = "r62K`ERW4n5dpybz<()eR~](&uQ=f)`yjtFXwNET{>8R?7GQXKtKG$<)Mt>h$$6"

db.init_app(app)

'''@app.cli.command('init-db')
def init_db():
    db.init_app(app)
    """Create all database tables."""
    with app.app_context():
        # Drop all tables and then create them (DANGEROUS: use for development only)
        # db.drop_all() 
        db.create_all()
        print("Database tables created!")''' #only activate while pushing in production



@app.route("/")
def home():
    return render_template("index.html")


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
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)