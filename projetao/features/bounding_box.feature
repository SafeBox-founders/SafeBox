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

  Scenario: Successfully edit a box
    Given I created a bounding box
    And I click on editar box
    And I fil the editar box fields
    When I click on confirmar edicao of box
    Then I see that the box was edited

  Scenario: Failed edit a box
    Given I created a bounding box
    And I click on editar box
    And I do not fill all box fields
    When I click on confirmar edicao of box
    Then I can see that the box was not edited


