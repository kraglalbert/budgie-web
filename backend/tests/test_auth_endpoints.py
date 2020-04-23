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
                },
            )
            self.assertEqual(resp.status_code, 200)

            # log in user
            resp = c.post(
                "/auth/login", json={"email": "jdoe@gmail.com", "password": "secret"},
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            token = json_data["token"]

            # get user by username
            resp = c.get(
                "/users/jdoe@gmail.com",
                headers={"Authorization": "Bearer {}".format(token)},
            )
            self.assertEqual(resp.status_code, 200)

            json_data = resp.get_json()
            self.assertTrue(json_data is not None)
            self.assertEqual(json_data["email"], "jdoe@gmail.com")

            # get user by ID
            user_id = json_data["id"]
            resp = c.get(
                "/users/{}".format(user_id),
                headers={"Authorization": "Bearer {}".format(token)},
            )
            self.assertEqual(resp.status_code, 200)
