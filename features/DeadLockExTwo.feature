Feature:  Asynchronous scenarios with borrowing and registering to events

  Scenario: Behavior of two users trying to borrow and register for event
    Given Library contain book bOne
    And pOne is logged into the terminal
    And pTwo is logged into the terminal
    And pOne borrows bOne
    When pTwo registers for eventOne with bOne
    And pOne register for eventOne without book request
    And pOne checksout book
    Then pTwo denied registration pOne registering and owns book