Feature: CRUD of ambiente
    Scenario: As a client of the system, I want to create a ambiente
        Given I am on the Home View
        When I click on Gerenciar câmeras 
        And I click on the criar ambiente button
        And I fill the criar ambiente fields
        And I click on the criar button
        Then I go to Meus ambientes view
        And I created a ambiente

    Scenario: As a client of the system, I want to view an existing ambiente
        Given I am on ambientes list view
        And There is a registered ambiente
        When I click on view a existing ambiente
        Then I go the existing ambiente detail page

    Scenario: As a client of the system, I want to deactivate an existing ambiente
        Given I am on ambientes list view
        And There is a registered ambiente
        When I click on desativar ambiente
        Then I can see that the ambiente was deactivated