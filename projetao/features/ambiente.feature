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

    Scenario: As a client of the system, I want to edit the ambiente name on the ambientes list
        Given I am on ambientes list view
        And There is a registered ambiente
        And I click on editar ambiente
        And I fill the name field
        And I click on confirmar edição
        And I am on ambientes list view
        Then I can see that the ambiente was edited

    Scenario: Edit the ambient name failed on the ambientes list
        Given I am on ambientes list view
        And There is a registered ambiente
        And I click on editar ambiente
        And I fill the repeated name field
        And I click on confirmar edição
        Then I can see that the ambiente was not edited

    Scenario: As a client of the system, I want to cancel while edit the ambiente
        Given I am on ambientes list view
        And There is a registered ambiente
        And I click on editar ambiente
        When I click on cancelar
        Then I am on ambientes list view