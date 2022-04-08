Feature: Assign a plan to my user account
    Scenario: As a client of the system, I want to assign a plan to my acount
        Given I am on the Profile View
        When I click on the Assinar plano button
        And I chose my plan 
        And I click on the Assinar button
        Then I go to my profile view
        And I assigned my plan

    Scenario: As a client of the system, I want to visualize my current signature
        Given I am on the Profile View
        And I have a signature
        When I click on the Visualizar Assinatura button
        Then I go to my signature view
        And I can see my current signature

    Scenario: As a client of the system, I want to edit my current signature
        Given I am on the Profile View
        And I have a signature
        When I click on the Visualizar Assinatura button
        Then I go to my signature view
        And I click on Trocar Plano
        And I chose my new plan
        And I click on Mudar de plano
        And I can see my new signature



