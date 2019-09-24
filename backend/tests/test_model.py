import unittest
from flask import current_app
from app import create_app, db
from app.models import User, Transaction
from decimal import *

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # prefix all test cases with "test_"
    def test_create_user(self):
        user = User(name="John Doe", username="jdoe", password="goodpass", monthly_budget=Decimal('500.00'))
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username="jdoe").first()
        self.assertTrue(user is not None)
        self.assertTrue(user.monthly_budget == Decimal('500.00'))

    def test_delete_user(self):
        user = User(name="John Doe", username="jdoe", password="goodpass", monthly_budget=Decimal('500.00'))
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username="jdoe").first()
        self.assertTrue(user is not None)

        db.session.delete(user)
        db.session.commit()

        user = User.query.filter_by(username="jdoe").first()
        self.assertTrue(user is None)
    