Feature: Highlighting race condition raised in software queue

  Scenario: 3 users entering lab after opening
    Given Lab initialized to be open in 10 seconds
    When PatronOne request to join before the lab is opened
    And PatronTwo request to join before the lab is opened
    And PatronThree request to join before the lab is opened
    Then The Lab has been opened
    And Confirm PatronOne and PatronTwo are the users in the Lab