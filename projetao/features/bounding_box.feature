Feature: CRUD of camera
  Scenario: As a client of the system, I want to create a bounding box
        Given I am at an Camera view
        When I fill the create bounding box fields
        And I click on criar bounding box
        Then I can see the created bounding box

   Scenario: As a client of the system, I want to see a bounding box information
      Given I am at an Camera view
      When I fill the create bounding box fields
      And I click on criar bounding box
      Then I can see the bounding box information


