Feature: Assign a plan to my user account
    Scenario: As a client of the system, I want to visualize my current signature
        Given I am on the Profile View
        When I click on the Visualizar Assinatura button
        Then I go to my signature view
        And I can see my current signature

    Scenario: As a client of the system, I want to edit my current signature
        Given I am on the Profile View
        When I click on the Visualizar Assinatura button
        Then I go to my signature view
        And I click on Trocar Plano
        And I chose my new plan
        And I click on Mudar de plano
        And I can see my new signature

    Scenario: As a cliente of the system, I want to remove the current signature
        Given I am on the Profile View
        When I click on the Visualizar Assinatura button
        Then I go to my signature view
        And I click on Remover Plano
        And I can see the message confirm
        And I click on confirm button 'OK'
        And I can see the Profile View


