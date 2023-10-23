import os
import unittest

from app import app
from models import QR_Code, QR_Code_Usage_Statistics, User, db

# Configure the app for testing
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/qrcode_generator_test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a testing database before each test."""
        with app.app_context():
            db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_signup(self):
        with app.app_context():
            user = User.signup("testuser", "testuser@example.com", "password")
            self.assertIsInstance(user, User)
            self.assertEqual(user.username, "testuser")
            self.assertEqual(user.email, "testuser@example.com")
            self.assertTrue(user.password.startswith("$2b$"))

    def test_authenticate_valid(self):
        with app.app_context():
            user = User.signup("testuser", "testuser@example.com", "password")
            authenticated_user = User.authenticate("testuser", "password")
            self.assertIsInstance(authenticated_user, User)
            self.assertEqual(authenticated_user.username, "testuser")
            self.assertEqual(authenticated_user.email, "testuser@example.com")

    def test_authenticate_invalid(self):
        with app.app_context():
            user = User.signup("testuser", "testuser@example.com", "password")
            authenticated_user = User.authenticate("testuser", "wrongpassword")
            self.assertFalse(authenticated_user)

class QRCodeModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a testing database before each test."""
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_create_qr_code(self):
        with app.app_context():
            user = User.signup("testuser", "testuser@example.com", "password")
            db.session.commit()
            qr_code = QR_Code(user_id=user.user_id, url="https://example.com")
            db.session.add(qr_code)
            db.session.commit()
            self.assertIsInstance(qr_code, QR_Code)
            self.assertEqual(qr_code.url, "https://example.com")

class QRCodeUsageStatisticsModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a testing database before each test."""
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_create_qr_code_usage_statistics(self):
        with app.app_context():
            user = User.signup("testuser", "testuser@example.com", "password")
            db.session.commit()
            qr_code = QR_Code(user_id=user.user_id, url="https://example.com")
            db.session.add(qr_code)
            db.session.commit()
            statistics = QR_Code_Usage_Statistics(qr_code_id=qr_code.qr_code_id, scanned_by="tester")
            db.session.add(statistics)
            db.session.commit()
            self.assertIsInstance(statistics, QR_Code_Usage_Statistics)
            self.assertEqual(statistics.scanned_by, "tester")

if __name__ == '__main__':
    unittest.main()
