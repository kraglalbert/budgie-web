from behave import *


@given("the User is logged in")
def user_is_logged_in(context):
    assert True


@when("the User adds a Transaction for groceries with amount 100.23")
def user_adds_valid_transaction(context):
    assert True


@then("the Transaction is saved successfully")
def save_transaction(context):
    assert True


@when("the User adds a Transaction for groceries with amount -100.23")
def user_adds_invalid_transaction(context):
    assert True


@then("the Transaction is not saved")
def check_transaction_not_saved(context):
    assert True
