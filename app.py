import os

from dotenv import load_dotenv
from flask import Flask, flash, g, redirect, render_template, session
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from forms import LoginForm, QRCodeForm, SignUpForm
from models import QR_Code, QR_Code_Usage_Statistics, User, connect_db, db

CURR_USER_KEY = "curr_user"

# Load environment variables
load_dotenv()

app = Flask(__name__)
cors = CORS(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/qrcode_generator"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "QRCode Generator"

connect_db(app)

# with app.app_context():
#     db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.user_id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# Routes

@app.route("/")
def home_page():
    """Display home page."""
    form = QRCodeForm()

    return render_template("home.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data,
                               password=form.password.data,
                               email=form.email.data)
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("signup.html", form=form)
        
        return redirect("/")

    else:
        return render_template("signup.html", form=form)


@app.route("/logout")
def logout():
    """Handle user logout."""

    if g.user:
        do_logout()
        flash("You have been logged out successfully.", "success")
    else:
        flash("You are not logged in.", "danger")
    
    return redirect("/")
    

@app.route("/profile")
def profile():
    """View user profile."""

    if g.user:
        return render_template("profile.html")
    else:
        flash("You are not logged in.", "danger")
    
    return redirect("/")