Feature:  Asynchronous scenarios with borrowing book

  Scenario: Two patron borrowing same book asynchronous
    Given Library contain book bOne
    And PatronOne is logged into the terminal
    And PatronTwo is logged into the terminal
    When PatronOne and PatronTwo borrows bOne simultaneously
    Then PatronOne persumed to be successful borrower