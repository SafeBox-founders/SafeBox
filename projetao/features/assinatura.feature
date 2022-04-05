Feature: Assign a plan to my user account
    Scenario: As a client of the system, I want to assign a plan to my acount
        Given I am on the Profile View
        When I click on the Assinar plano button
        And I chose my plan 
        And I click on the Assinar button
        Then I go to my profile view
        And I assigned my plan