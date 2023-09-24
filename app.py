import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_cors import CORS

from forms import QRCodeForm, LoginForm
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
    """Display home page"""
    form = QRCodeForm()

    return render_template("home.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    return render_template("login.html", form=form)
