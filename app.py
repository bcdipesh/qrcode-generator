import os
from dotenv import load_dotenv

from models import User, QR_Code, QR_Code_Usage_Statistics, connect_db, db

from flask import Flask, render_template

# Load environment variables
load_dotenv()

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/qrcode_generator"
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

# with app.app_context():
#     db.create_all()


# Routes


@app.route("/")
def home_page():
    """Display home page"""

    return render_template("home.html")


@app.route("/about")
def about_page():
    """Display about page"""

    return render_template("about.html")
