import os
import sys
import pdb

from time import sleep
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","projetao.settings")
django.setup()
sys.path.append("/home/battist/PycharmProjects/SafeBox")
from os import path
from behave import *
from pandas import options
from selenium import webdriver
from safebox.models import Cliente

use_step_matcher("re")

@given("I am on the Cadastrar Cliente View")
def step_impl(context):
    context.browser = webdriver.Chrome()
    context.browser.get("http://127.0.0.1:8000/")
    button = context.browser.find_element_by_name("cadastrar")
    button.click()

@given("I fill all fields")
def step_impl(context):
    cliente = Cliente.objects.all()
    variavel_id = 10000000000+len(cliente)+1
    nome = context.browser.find_element_by_name("nome")
    nome.send_keys("Testador")
    email = context.browser.find_element_by_name("email")
    email.send_keys("email@" + str(variavel_id) + ".com")
    contato = context.browser.find_element_by_name("contato")
    contato.send_keys("00078795455")
    cpf_cnpj = context.browser.find_element_by_name("cpf_cnpj")
    cpf_cnpj.send_keys(variavel_id)
    senha = context.browser.find_element_by_name("senha")
    senha.send_keys("123456")

@when("I click on the Submit button")
def step_impl(context):
    button = context.browser.find_element_by_name("cadastro")
    button.click()

@then("I create my profile")
def step_impl(context):
    cliente = Cliente.objects.all()
    variavel_id = 10000000000+len(cliente)+1
    assert cliente.filter(email=("email@" + str(variavel_id) + ".com"))  != []

@then("I go to Login page")
def step_impl(context):
    assert context.browser.title=="Login"

#=================================================================================================================
   
@then("stay in the Cadastrar Cliente View")
def step_impl(context):
    assert context.browser.title=="Cadastrar-se"

@given("I do not fill all fields")
def step_impl(context):
    nome = context.browser.find_element_by_name("nome")
    nome.send_keys("Testador_Cadastro_Falso")
    email = context.browser.find_element_by_name("email")
    email.send_keys("cadastro_falso30email.com")
    contato = context.browser.find_element_by_name("contato")
    contato.send_keys("0123456")
    senha = context.browser.find_element_by_name("senha")
    senha.send_keys("123456")

@then("I do not create my profile")
def step_impl(context):
    try:
        cliente = Cliente.objects.all()
        cliente.filter(email="cadastro_falso30email.com")
        assert True
    except:
        assert False


#=========================================================================================================
@Given("I am registered user")
def step_impl(context):
    context.execute_steps(u"""
    given Eu sou um usuario cadastrado
    and Eu estou na tela de login
    and Eu preencho o campo email e senha
    when Eu pressiono o botao "Logar"
    then Eu vejo que estou logado""")


@Given("I access the profile view")
def step_impl(context):
    button = context.browser.find_element_by_name("visualizar_perfil")
    button.click()
    context.browser.title == "Meu Perfil"

@When("I click Desativar Conta")
def step_impl(context):
    button = context.browser.find_element_by_name("desativar")
    button.click()

@Then("I deactivate my profile")
def step_impl(context):
    cliente = Cliente.objects.all()
    assert cliente.filter(email="delete3@email.com", active=False) != []

@Then("go to Cadastrar Cliente view")
def step_impl(context):
    assert context.browser.title == "Cadastrar-se"

#EDITAR CONTA

@When('I click on Editar Conta')
def step_impl(context):
    button = context.browser.find_element_by_name("editar")
    button.click()

@when("I fill all fields")
def step_impl(context):
    global atts_dictionary
    cliente = Cliente.objects.all()
    variavel_id = 20000000000+len(cliente)+1

    atts_dictionary = {'Email': "email@" + str(variavel_id) + ".com",
                       'Nome': 'Testador_editado',
                       'Contato': str(variavel_id),
                       'CPF | CNPJ': str(variavel_id),
                       'Senha': '654321',
                       'Ativo': True}

    nome = context.browser.find_element_by_name("nome")
    nome.clear()
    nome.send_keys(atts_dictionary['Nome'])
    email = context.browser.find_element_by_name("email")
    email.clear()
    email.send_keys(atts_dictionary['Email'])
    contato = context.browser.find_element_by_name("contato")
    contato.clear()
    contato.send_keys(atts_dictionary['Contato'])
    cpf_cnpj = context.browser.find_element_by_name("cpf_cnpj")
    cpf_cnpj.clear()
    cpf_cnpj.send_keys(atts_dictionary['CPF | CNPJ'])
    senha = context.browser.find_element_by_name("senha")
    senha.clear()
    senha.send_keys(atts_dictionary['Senha'])

@When('I click on Editar')
def step_impl(context):
    button = context.browser.find_element_by_name("editar")
    button.click()

@Then('I go to my profile view')
def step_impl(context):
    assert context.browser.title == "Meu Perfil"

@Then('I can see that my profile has changed')
def step_impl(context):
    div = context.browser.find_element_by_id("div_client_info")
    textos = (div.text).split("\n")
    atts_dictionary_novo = {}
    for i in range(len(textos)):
        if(textos[i] != "" and (":" in textos[i])):
            atts_dictionary_novo[textos[i].split(": ")[0]] = textos[i].split(": ")[1]
    #atts_dictionary_novo = {textos[i].split(": ")[0]: textos[i].split(": ")[1] for i in range(len(textos))}
    atts_dictionary_novo.pop('Cadastrou-se em')
    atts_dictionary_novo.pop('Última atualização')
    atts_dictionary_novo.pop('Ativo')
    for key in atts_dictionary_novo.keys():
        assert atts_dictionary_novo[key] == atts_dictionary[key]

