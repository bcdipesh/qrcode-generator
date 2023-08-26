import os
from dotenv import load_dotenv

from flask import Flask

# Load environment variables
load_dotenv()

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/qrcode_generator"
app.config["SQLALCHEMY_ECHO"] = True
