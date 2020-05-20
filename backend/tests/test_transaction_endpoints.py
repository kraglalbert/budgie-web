import unittest
import datetime
from flask import current_app, request, jsonify
from app.models import User
from app import create_app, db

TITLE = "Groceries"
SOURCE = "Safeway"
AMOUNT = -10045
YEAR = 2019
MONTH = 11
DAY = 1
CURRENCY = "CAD"
CATEGORY = "None"


class TransactionsIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_get_transaction(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/auth/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post(
                "/transactions",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "currency": CURRENCY,
                    "category": CATEGORY,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]

            # get all transactions
            resp = c.get("/transactions")
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transaction by ID
            resp = c.get("/transactions/{}".format(t_id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(json_data["amount"], AMOUNT)
            self.assertEqual(json_data["source"], SOURCE)

            # get all transactions for user ID
            resp = c.get("/transactions/user/{}?currency={}".format(user.id, CURRENCY))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, valid
            resp = c.get(
                "/transactions/user/{}?year={}&month={}&currency={}".format(
                    user.id, YEAR, MONTH, CURRENCY
                )
            )
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, year only
            resp = c.get(
                "/transactions/user/{}?year={}&currency={}".format(
                    user.id, YEAR, CURRENCY
                )
            )
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, wrong date
            resp = c.get(
                "/transactions/user/{}?year={}&month={}&currency={}".format(
                    user.id, YEAR, MONTH - 1, CURRENCY
                )
            )
            json_data = resp.get_json()
            self.assertEqual(json_data, [])

            # get transactions for user by date, bad format
            resp = c.get("/transactions/user/{}?month={}".format(user.id, MONTH))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 400)

    def test_create_transaction_invalid(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/auth/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            # create with invalid date
            resp = c.post(
                "/transactions",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": 1000,
                    "email": user.email,
                    "currency": CURRENCY,
                    "category": CATEGORY,
                    "year": 0,
                    "month": 0,
                    "day": 0,
                },
            )
            self.assertEqual(resp.status_code, 400)

            # create with empty fields
            resp = c.post(
                "/transactions",
                json={
                    "title": "",
                    "source": "",
                    "amount": 0,
                    "email": "",
                    "currency": "",
                    "category": "",
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 400)

    def test_update_transaction(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/auth/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post(
                "/transactions",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "currency": CURRENCY,
                    "category": CATEGORY,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]
            json_data["title"] = "New Car"
            json_data["source"] = "Tesla"
            json_data["amount"] = -5000000
            json_data["year"] = 2020
            json_data["month"] = 1
            json_data["day"] = 31

            resp = c.put("/transactions/{}".format(t_id), json=json_data)
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            self.assertEqual(json_data["title"], "New Car")
            self.assertEqual(json_data["source"], "Tesla")
            self.assertEqual(json_data["amount"], -5000000)

    def test_delete_transaction(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/auth/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            csrf_access_token = ""
            for cookie in c.cookie_jar:
                if cookie.name == "csrf_access_token":
                    csrf_access_token = cookie.value

            resp = c.post(
                "/transactions",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "currency": CURRENCY,
                    "category": CATEGORY,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]

            # delete existing transaction
            resp = c.delete("/transactions/{}".format(t_id),)
            self.assertEqual(resp.status_code, 200)

            # try deleting non-existent transaction
            resp = c.delete("/transactions/{}".format(t_id),)
            self.assertEqual(resp.status_code, 404)
