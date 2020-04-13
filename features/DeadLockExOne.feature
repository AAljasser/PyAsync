Feature:  Asynchronous scenarios with borrowing book

  Scenario: Behavior of two users trying to borrow and checkout same book
    Given Library contain book bOne
    And pOne is logged into the terminal
    And pTwo is logged into the terminal
    And pOne borrows bOne
    When pOne checks out cart books before pTwo tries to borrow bOne
    Then pOne gets the book and pTwo receives unavailable book
    And pTwo sends a checkout request and nothing is taken