Feature: Test new cliente can be added in the Safebox
    Scenario: We can add a cliente with valids fields
        Given I am on the Cadastrar Cliente View
        And I fill all fields
        When I click on the Submit button
        Then I create my profile 
        And go to my Profile View
    
    Scenario: We can not add a cliente with an invalid field
        Given I am on the Cadastrar Cliente View
        And I do not fill all fields
        When I click on the Submit button
        Then I do not create my profile
        And stay in the Cadastrar Cliente View
    
    Scenario: Deactivate a existent client in the Safebox
        Given I am registered user
        And I am at the profile view
        When I click Desativar Conta
        Then I deactivate my profile
        And go to Cadastrar Cliente view
