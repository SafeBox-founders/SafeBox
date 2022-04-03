Feature: Login Cliente
  Como usuario do sistema
  Eu gostaria de fazer o login na minha conta
  Podendo assim ter acesso ao sistema como um todo

  # TA_01
  Scenario: Login de usuario cadastrado
    Given Eu sou um usuario cadastrado
    And Eu estou na tela de login
    And Eu preencho o campo email e senha
    When Eu pressiono o botao "Logar"
    Then Eu vejo que estou logado

  # TA_02
  Scenario: Usuario nao cadastrado tentando fazer login
    Given Eu estou na tela de login
    And Eu preencho o campo email e senha com dados nao cadastrados
    When Eu pressiono o botao "Logar"
    Then Eu vejo a mensagem de erro

  Scenario: Deslogar usuario logado
    Given Eu sou um usuario cadastrado
    And Eu estou logado
    And Eu estou na tela de home
    When Eu pressiono o botao sair
    And Eu estou na tela de login