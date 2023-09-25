import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from forms import LoginForm, QRCodeForm, SignUpForm
from models import QR_Code, QR_Code_Usage_Statistics, User, connect_db, db

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

    
