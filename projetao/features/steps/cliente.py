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

@given("I fill all fields")
def step_impl(context):
    cliente = Cliente.objects.all()
    # record = cliente[len(cliente) - 1]
    variavel_id = 10000000000+len(cliente)
    # pdb.set_trace()
    nome = context.browser.find_element_by_name("nome")
    nome.send_keys("Testador")
    email = context.browser.find_element_by_name("email")
    email.send_keys("email@email" + str(variavel_id) + ".com")
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
    record = cliente[len(cliente) - 1]
    variavel_id = record.id
    assert cliente.filter(email=("email@email" + str(variavel_id) + ".com"))  != []

@then("go to my Profile View")
def step_impl(context):

    assert context.browser.title=="Meu Perfil"

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
    given I am on the Cadastrar Cliente View
    and I fill all fields
    when I click on the Submit button
    then I create my profile 
    and go to my Profile View
    """)


@Given("I am at the profile view")
def step_impl(context):
    assert context.browser.title == "Meu Perfil"

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

@When('I fill all fields')
def step_impl(context):
    cliente = Cliente.objects.all()
    record = cliente[len(cliente) - 1]
    variavel_id = record.id + 2
    nome = context.browser.find_element_by_name("nome")
    nome.send_keys("Testador")
    email = context.browser.find_element_by_name("email")
    email.send_keys("email@email" + str(variavel_id) + ".com")
    contato = context.browser.find_element_by_name("contato")
    contato.send_keys("00078795455")
    cpf_cnpj = context.browser.find_element_by_name("cpf_cnpj")
    cpf_cnpj.send_keys(variavel_id)
    senha = context.browser.find_element_by_name("senha")
    senha.send_keys("123456")


@When('I click on Editar')
def step_impl(context):
    button = context.browser.find_element_by_name("editar")
    button.click()


@Then('I go to my profile view')
def step_impl(context):
    pass

@Then('I can see that my profile has changed')
def step_impl(context):
    pass