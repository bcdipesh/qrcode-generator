"""SQLAlchemy models for QRCode Generator"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """Represents the users in the system"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(50), nullable=False, unique=True)

    email = db.Column(db.String(50), nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.
        
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False

class QR_Code(db.Model):
    """Represents the qr codes created by the users"""

    __tablename__ = "qr_codes"

    qr_code_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    url = db.Column(db.Text, nullable=False)


class QR_Code_Usage_Statistics(db.Model):
    """Represents the qr code usage statistics"""

    __tablename__ = "qr_code_usage_statistics"

    usage_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    qr_code_id = db.Column(
        db.Integer, db.ForeignKey("qr_codes.qr_code_id"), nullable=False
    )

    scan_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    scanned_by = db.Column(db.String(50), nullable=False)


def connect_db(flask_app):
    """Connect this database to provided Flask app"""

    db.app = flask_app
    db.init_app(flask_app)
