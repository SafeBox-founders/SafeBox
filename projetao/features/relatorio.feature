Feature: Create, view and download Relatorio
  Scenario: As a client of the system, i want to generate report in certain period of time
    Given I am on Relatorio view
    And I click on Relatorios
    And I click on Gerar Relatorio
    And I insert the initial and final dates
    When I click on Criar Relatorio
    Then I see that the report was created

  Scenario: As a client of the system, i want to download the report
    Given I created a relatorio
    When I click on Exportar Relatorio
    Then I see that the report was downloaded

  Scenario: As a client of the system, i want to access the report history
    Given I created a relatorio
    And I am on Relatorio view
    And I click on Relatorios
    When I click on Historico of the report
    Then I see the report history