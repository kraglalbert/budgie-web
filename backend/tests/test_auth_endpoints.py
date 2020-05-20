import unittest
import datetime
from flask import current_app, request, jsonify
from app.models import User
from app import create_app, db


class AuthIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_get_user(self):
        with self.app.test_client() as c:
            resp = c.post(
                "/auth/register",
                json={
                    "name": "John Doe",
                    "email": "jdoe@gmail.com",
                    "password": "secret",
                    "default_currency": "CAD",
                },
            )
            self.assertEqual(resp.status_code, 200)

            # log in user
            resp = c.post(
                "/auth/login", json={"email": "jdoe@gmail.com", "password": "secret"},
            )
            self.assertEqual(resp.status_code, 200)

            # get user by username
            resp = c.get("/users/jdoe@gmail.com")
            self.assertEqual(resp.status_code, 200)

            json_data = resp.get_json()
            self.assertTrue(json_data is not None)
            self.assertEqual(json_data["email"], "jdoe@gmail.com")

            # get user by ID
            user_id = json_data["id"]
            resp = c.get("/users/{}".format(user_id))
            self.assertEqual(resp.status_code, 200)

    def test_csrf(self):
        self.app.config["JWT_COOKIE_CSRF_PROTECT"] = True
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/auth/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post("/auth/logout")
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.get_json(), {"msg": "Missing CSRF token"})

            # get CSRF token and pass it as a header
            csrf_access_token = ""
            for cookie in c.cookie_jar:
                if cookie.name == "csrf_access_token":
                    csrf_access_token = cookie.value

            resp = c.post("/auth/logout", headers={"X-CSRF-TOKEN": csrf_access_token})
            self.assertEqual(resp.status_code, 200)

    def test_non_matching_csrf_token(self):
        self.app.config["JWT_COOKIE_CSRF_PROTECT"] = True
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/auth/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post("/auth/logout", headers={"X-CSRF-TOKEN": "fake token"})
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(
                resp.get_json(), {"msg": "CSRF double submit tokens do not match"}
            )
