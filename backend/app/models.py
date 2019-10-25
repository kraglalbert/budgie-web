import json
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # amount in cents
    monthly_budget = db.Column(db.Integer)
    transactions = db.relationship("Transaction", backref="users", lazy=True)
    transactions_months = db.relationship("TransactionMonth", backref="users", lazy=True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_test_user():
        user = User(name="Albert Kragl", username="akragl")
        db.session.add(user)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "password_hash": self.password_hash,
            "monthly_budget": self.monthly_budget if self.monthly_budget is not None else 0,
            "transactions": Transaction.serialize_list(self.transactions),
            "username": self.username,
        }

    @staticmethod
    def serialize_list(users):
        json_users = []
        for user in users:
            json_users.append(user.serialize)
        return json_users

    def __repr__(self):
        return "<User %r>" % self.username


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False, nullable=False)
    source = db.Column(db.String(64))
    # amount in cents
    amount = db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transaction_month_id = db.Column(db.Integer, db.ForeignKey("transaction_months.id"), nullable=False)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "amount": self.amount,
            "date": self.date,
            "user_id": self.user_id,
            "transaction_month_id": self.transaction_month_id
        }

    @staticmethod
    def serialize_list(transactions):
        json_transactions = []
        for t in transactions:
            json_transactions.append(t.serialize)
        return json_transactions

    def __repr__(self):
        return "<Transaction %r>" % self.title

class TransactionMonth(db.Model):
    __tablename__ = "transaction_months"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transactions = db.relationship("Transaction", backref="transaction_months", lazy=True)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "date": self.date,
            "transactions": self.transactions,
        }

    @staticmethod
    def serialize_list(transaction_months):
        json_transactions_months = []
        for tm in transactions_months:
            json_transactions_months.append(tm.serialize)
        return json_transactions_months

    def __repr__(self):
        return "<TransactionMonth %r>" % self.title
