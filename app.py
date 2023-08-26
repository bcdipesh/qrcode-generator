import os
from dotenv import load_dotenv

from models import User, QR_Code, QR_Code_Usage_Statistics, connect_db, db

from flask import Flask

# Load environment variables
load_dotenv()

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/qrcode_generator"
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()
