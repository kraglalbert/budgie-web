import unittest
from flask import current_app, request, jsonify
from app.models import User
from app import create_app, db


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_users_empty(self):
        with self.app.test_client() as c:
            resp = c.get("/users")
            json_data = resp.get_json()
            self.assertTrue(json_data is not None)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(json_data, [])

    def test_user_not_found(self):
        with self.app.test_client() as c:
            resp = c.get("/users/jdoe")
            self.assertEqual(resp.status_code, 404)

    def test_create_and_get_user(self):
        with self.app.test_client() as c:
            resp = c.post(
                "/users/create",
                json={
                    "name": "John Doe",
                    "email": "jdoe@gmail.com",
                    "password": "secret",
                },
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

    def test_create_and_get_transaction(self):
        user = User.generate_test_user()
        TITLE = "Groceries"
        SOURCE = "Safeway"
        AMOUNT = 10045
        YEAR = 2019
        MONTH = 11
        DAY = 1

        with self.app.test_client() as c:
            resp = c.post(
                "/transactions/create",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]

            # get transaction by ID
            resp = c.get("/transactions/{}".format(t_id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(json_data["amount"], AMOUNT)
            self.assertEqual(json_data["source"], SOURCE)

            # get all transactions for user ID
            resp = c.get("/transactions/user/{}".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, valid
            resp = c.get("/transactions/user/{}?year=2019&month=11".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, year only
            resp = c.get("/transactions/user/{}?year=2019".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, wrong date
            resp = c.get("/transactions/user/{}?year=2019&month=10".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 400)

            # get transactions for user by date, bad format
            resp = c.get("/transactions/user/{}?month=10".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 400)
