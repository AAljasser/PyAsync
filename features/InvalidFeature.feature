Feature: Acceptance Test Suite Valid paths

  Background: Server is executed

  Scenario: Entering invalid id for staff login
    Given User ID will be used doesn't exists
    When User attempts to login as staff with invalid ID
    Then Terminal will response with a decline and require valid ID

  Scenario: Patron borrowing non-existing book
    Given that non-existing book isn't in Library
    When Patron request borrow of Non-existing book
    Then System will deny due to non-existing

  Scenario: Patron checkout a book that has been unchecked
    Given Patron sent 'borrow,b1000' command
    And Patron sends 'uncheck,b1000' command
    When Patron send checkout command
    Then Patron doesn't checkout the b1000

  Scenario: Patron checkout a book that has been unchecked (15 sec) by the automated system
    Given Patron sent 'borrow,b1000' command
    And wait until automated system executed removal of book
    When Patron send checkout command
    Then Patron doesn't checkout the b1000