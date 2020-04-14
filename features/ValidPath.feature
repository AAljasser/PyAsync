Feature: Acceptance Test Suite Valid paths

  Background: Server is executed

  Scenario: Staff member creation of a Patron
    Given Staff member logged into terminal
    When Staff sends 'crpatron,p2020,NAME' command
    Then Validate 'p2020' has been created

  Scenario: Patron Borrowing a Book
    Given Patron logged into terminal
    And book 'b1001' exists
    When Patron send 'borrow,b1001' command
    And Patron send 'checkout' command
    Then Validate Patron has taken the b1001
    And Validate Library removal of b1001

  Scenario: Patron registration of newly created Event with book b2020
    Given Staff creating e2020 using 'crevent,e2020' command
    And Patron failed attempt to register to event with non existing book b2020
    When Staff create Book 'addbook,b2020,TestingScenarioBook'
    And Patron reattempt to register to event with b2020 using 'event,e2020,b2020'
    Then Validate Patron registration and acquiring of book

  Scenario: Patron Listing Available Labs
    Given Patron loged into terminal
    When Patron types 'lab'
    Then Patron recieves a list of available labs

  Scenario: Two Patron queue to unopned lab (Will take time to finish)
    Given Staff creating a lab to be opened 'clab,l2020'
    When Patron One joins lab using 'lab,l2020'
    And Patron Two joins lab using 'lab,l2020'
    Then Validate Patron's entrance