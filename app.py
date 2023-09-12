import os
from pprint import pprint

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from forms import QRCodeForm
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



