Feature: CRUD of ambiente
    Scenario: As a client of the system, I want to create a ambiente
        Given I am on the Home View
        When I click on Gerenciar câmeras 
        And I click on the criar ambiente button
        And I fill the criar ambiente fields
        And I click on the criar button
        Then I go to Criar ambiente view
        And I created a ambiente