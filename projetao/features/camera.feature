Feature: CRUD of ambiente
    Scenario: As a client of the system, I want to create a camera
        Given I am at an Ambiente view
        When I click on Adicionar nova câmera 
        And I fill the criar camera fields
        And I click on the criar camera button
        Then I go back to an existing ambiente detail page
        And I created a camera

    Scenario: As a client of the system, I want to view a camera
        Given I have a created camera
        When I click on visualizar camera
        Then I go to the camera view