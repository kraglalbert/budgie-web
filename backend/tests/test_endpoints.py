import unittest
from flask import current_app, request, jsonify
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
            resp = c.get('/users')
            json_data = resp.get_json()
            self.assertTrue(json_data is not None)
            self.assertEqual(json_data, [])
