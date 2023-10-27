import json
import os
import unittest

from dotenv import load_dotenv

from app import CURR_USER_KEY, app, db
from models import QR_Code, User

# Load environment variables
load_dotenv()

# Configure the app for testing
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/qrcode_generator_test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True
app.config["WTF_CSRF_ENABLED"] = False

class ProfileRouteTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and create a user for testing."""
        self.client = app.test_client()

        # Create a user for testing
        with app.app_context():
            db.create_all()
            user = User.signup(username="testuser1", password="password", email="testuser1@example.com")
            db.session.commit()
        
    def tearDown(self):
        """Clean up after the test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_signup_route_with_valid_data(self):
        """Test the signup route with valid user data."""
        with self.client as c:
            response = c.post("/signup", data={"username": "testuser", "password": "password", "email": "testuser@example.com"})
            user = User.query.filter_by(username="testuser").first()

            self.assertTrue(user)  # Check if the user was created in the database
            self.assertEqual(response.status_code, 302)  # Check for a redirect

    def test_signup_route_with_duplicate_username(self):
        """Test the signup route with a duplicate username."""
        # Create a user with the same username to simulate a duplicate username
        with app.app_context():
            user = User.signup("testuser", "password", "testuser@example.com")
            db.session.commit()

        with self.client as c:
            response = c.post("/signup", data={"username": "testuser", "password": "password123", "email": "testuser2@example.com"})
            user_count = User.query.filter_by(username="testuser").count()

            self.assertEqual(user_count, 1)  # Ensure there is only one user with this username
            self.assertEqual(response.status_code, 200)  # Expect the same page to be rendered
    
    def test_login_with_valid_credentials(self):
        """Test the login route with valid user credentials."""
        # Create a test user
        with app.app_context():
            user = User.signup(username="testuser", password="password", email="testuser@example.com")
            db.session.commit()

        with self.client as c:
            response = c.post("/login", data={"username": "testuser", "password": "password"}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("Hello, testuser!", html)
            self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_credentials(self):
        """Test the login route with invalid user credentials."""
        with self.client as c:
            response = c.post("/login", data={"username": "testuser", "password": "wrongpassword"})
            html = response.get_data(as_text=True)

            self.assertIn("Invalid credentials.", html)
            self.assertEqual(response.status_code, 200)

    def test_profile_route_with_authenticated_user(self):
        """Test the profile route with an authenticated user."""
        with self.client as c:
            with c.session_transaction() as sess:
                # Log in the user
                sess[CURR_USER_KEY] = 1

            response = c.get("/user/profile")
            html = response.get_data(as_text=True)

            self.assertIn("User Profile", html)
            self.assertIn("testuser1", html)
            self.assertIn("testuser1@example.com", html)
            self.assertEqual(response.status_code, 200)

    def test_profile_route_with_unauthenticated_user(self):
        """Test the profile route with an unauthenticated user."""
        with self.client as c:
            response = c.get("/user/profile")

            # Check for a redirect to the login page
            self.assertTrue(response.location.endswith("/"))
            self.assertEqual(response.status_code, 302)
    
    def test_logout_with_authenticated_user(self):
        """Test the logout route with an authenticated user."""
        with self.client as c:
            with c.session_transaction() as sess:
                # Log in the user
                sess[CURR_USER_KEY] = 1

            response = c.get("/logout", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("You have been logged out successfully.", html)
            self.assertEqual(response.status_code, 200)

    def test_logout_with_unauthenticated_user(self):
        """Test the logout route with an unauthenticated user."""
        with self.client as c:
            response = c.get("/logout", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("You are not logged in.", html)
            self.assertEqual(response.status_code, 200)
    
    def test_save_qr_code_with_authenticated_user(self):
        """Test the save_qr_code route with an authenticated user."""
        # Create a test user and log them in
        with self.client as c:
            with c.session_transaction() as sess:
                # Log in the user
                sess[CURR_USER_KEY] = 1

            # JSON data to simulate the POST request
            json_data = {"qrCodeUrl": "https://example.com/qr-code"}

            response = c.post("/user/qrcode", json=json_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("Your QR Code has been saved successfully.", html)
            self.assertEqual(response.status_code, 200)

    def test_save_qr_code_with_unauthenticated_user(self):
        """Test the save_qr_code route with an unauthenticated user."""
        # JSON data to simulate the POST request 
        json_data = {"qrCodeUrl": "https://example.com/qr-code"}

        with self.client as c:
            response = c.post("/user/qrcode", json=json_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("Access unauthorized.", html)
            self.assertEqual(response.status_code, 200)
    
    def test_list_qr_codes_with_authenticated_user(self):
        """Test the list_qr_codes route with an authenticated user."""
        # Create a test user, log in, and add some QR codes
        with app.app_context():
            user = User.query.get_or_404(1)
            qr_code1 = QR_Code(user_id=user.user_id, url="https://example.com/qr-code-1")
            qr_code2 = QR_Code(user_id=user.user_id, url="https://example.com/qr-code-2")
            db.session.add_all([qr_code1, qr_code2])
            db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                # Log in the user
                sess[CURR_USER_KEY] = 1

            response = c.get("/user/qrcode")
            html = response.get_data(as_text=True)

            self.assertIn("Total: 2", html)
            self.assertEqual(response.status_code, 200)

    def test_list_qr_codes_with_unauthenticated_user(self):
        """Test the list_qr_codes route with an unauthenticated user."""
        with self.client as c:
            response = c.get("/user/qrcode", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("Access unauthorized.", html)
            self.assertEqual(response.status_code, 200)
    
    def test_delete_qr_code_with_authenticated_user(self):
        """Test the delete_qr_code route with an authenticated user."""
        # Create a test user, log them in, and add a QR code
        with app.app_context():
            user = User.query.get_or_404(1)
            qr_code = QR_Code(user_id=user.user_id, url="https://example.com/qr-code-1")
            db.session.add(qr_code)
            db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                # Log in the user
                sess[CURR_USER_KEY] = 1

            response = c.post(f"/user/qrcode/1/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("Your QR Code has been deleted.", html)
            self.assertEqual(response.status_code, 200)

    def test_delete_qr_code_with_unauthenticated_user(self):
        """Test the delete_qr_code route with an unauthenticated user."""
        # Create a test QR code
        with app.app_context():
            qr_code = QR_Code(user_id=1, url="https://example.com/qr-code-1")
            db.session.add(qr_code)
            db.session.commit()

        with self.client as c:
            response = c.post(f"/user/qrcode/1/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("Access unauthorized.", html)
            self.assertEqual(response.status_code, 200)
    
    def test_update_qr_code_form_with_authenticated_user(self):
        """Test the update_qr_code_form route with an authenticated user."""
        # Create a test user, log them in, and add a QR code
        with app.app_context():
            qr_code = QR_Code(user_id=1, url="https://example.com/qr-code-1")
            db.session.add(qr_code)
            db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                # Log in the user
                sess[CURR_USER_KEY] = 1

            response = c.get(f"/user/qrcode/1/update")
            html = response.get_data(as_text=True)

            self.assertIn("Update QRCode", html)
            self.assertEqual(response.status_code, 200)
    
    def test_update_qr_code_form_with_unauthenticated_user(self):
        """Test the update_qr_code_form route with an unauthenticated user."""
        # Create a test QR code
        with app.app_context():
            qr_code = QR_Code(user_id=1, url="https://example.com/qr-code-1")
            db.session.add(qr_code)
            db.session.commit()

        with self.client as c:
            response = c.get(f"/user/qrcode/1/update", follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertIn("Access unauthorized.", html)
            self.assertEqual(response.status_code, 200)