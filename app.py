import os
from pprint import pprint

from dotenv import load_dotenv
from flask import Flask, render_template

from forms import QRCodeForm
from models import QR_Code, QR_Code_Usage_Statistics, User, connect_db, db

# Load environment variables
load_dotenv()

app = Flask(__name__)

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


@app.route("/generate-qr-code", methods=["POST"])
def generate_qr_code():
    """
        Generate a QR Code using the free API
    """
    
    form = QRCodeForm()
    
    if form.validate_on_submit():
        # Process the form data
        content = form.content.data
        size = form.size.data
        charset_source = form.charset_source.data
        charset_target = form.charset_target.data
        ecc = form.ecc.data
        color = form.color.data
        bg_color = form.bg_color.data
        margin = form.margin.data
        qzone = form.qzone.data
        file_format = form.file_format.data
        
        pprint(form.data)
    
    return render_template("home.html", form=form)
    

