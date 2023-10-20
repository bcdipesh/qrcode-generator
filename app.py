import os

from dotenv import load_dotenv
from flask import Flask, flash, g, redirect, render_template, request, session
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from forms import LoginForm, QRCodeForm, SignUpForm, UserEditForm
from models import QR_Code, QR_Code_Usage_Statistics, User, connect_db, db

CURR_USER_KEY = "curr_user"

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

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


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
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
        
        except IntegrityError:
            flash("Username/E-mail already taken", "danger")
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
    

@app.route("/user/profile", methods=["GET", "POST"])
def profile():
    """Update user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data

            db.session.commit()
            flash("Profile updated!", "success")
            return redirect(f"/user/profile")
        else:
            flash("Password incorrect!", "danger")
            return redirect("/")
    
    return render_template("profile.html", form=form)


@app.route("/user/qrcode", methods=["POST"])
def save_qr_code():
    """Save user QR Code."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    qr_code_url = request.json["qrCodeUrl"]

    qr_code = QR_Code(user_id = user.user_id, url = qr_code_url)

    db.session.add(qr_code)
    db.session.commit()

    flash("Your QR Code has been saved successfully.", "success")
    return redirect("/")


@app.route("/user/qrcode", methods=["GET"])
def list_qr_codes():
    """Display user qr codes."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    qr_codes = g.user.qr_codes
    return render_template("qrcode.html", qr_codes=qr_codes)


@app.route("/user/qrcode/<int:qr_code_id>/delete", methods=["POST"])
def delete_qr_code(qr_code_id):
    """Delete a qr code."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    qr_code = QR_Code.query.get_or_404(qr_code_id)
    if qr_code.user_id != g.user.user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    db.session.delete(qr_code)
    db.session.commit()

    flash("Your QR Code has been deleted.", "success")

    return redirect("/user/qrcode")
    

