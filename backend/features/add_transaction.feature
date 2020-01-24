Feature: the User can add a new Transaction

    Scenario: add a valid Transaction
        Given the User is logged in
        When the User adds a Transaction for groceries with amount 100.23
        Then the Transaction is saved successfully

    Scenario: invalid Transaction
        Given the User is logged in
        When the User adds a Transaction for groceries with amount -100.23
        Then the Transaction is not saved