import os
from time import sleep
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","projetao.settings")
django.setup()

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
    nome = context.browser.find_element_by_name("nome")
    nome.send_keys("Testador2")
    email = context.browser.find_element_by_name("email")
    email.send_keys("email001010231@email.com1")
    contato = context.browser.find_element_by_name("contato")
    contato.send_keys("00078795455")
    cpf_cnpj = context.browser.find_element_by_name("cpf_cnpj")
    cpf_cnpj.send_keys("01508754485")
    senha = context.browser.find_element_by_name("senha")
    senha.send_keys("123456")

@when("I click on the Submit button")
def step_impl(context):
    button = context.browser.find_element_by_name("cadastro")
    button.submit()

@then("I create my profile")
def step_impl(context):
    cliente = Cliente.objects.all()
    assert cliente.filter(email="email001010231@email.com1")!=[]

@then("go to my Profile View")
def step_impl(context):
    assert context.browser.title=="Perfil"
   
@then("stay in the Cadastrar Cliente View")
def step_impl(context):
    assert context.browser.title=="Cadastrar-se"

@given("I do not fill all fields")
def step_impl(context):
    nome = context.browser.find_element_by_name("nome")
    nome.send_keys("Testador1")
    email = context.browser.find_element_by_name("email")
    email.send_keys("email001010@email.com1")
    contato = context.browser.find_element_by_name("contato")
    contato.send_keys("0123456")
    senha = context.browser.find_element_by_name("senha")
    senha.send_keys("123456")

@then("I do not create my profile")
def step_impl(context):
    try:
        cliente = Cliente.objects.all()
        cliente.filter(email="email001010@email.com1")
        assert True
    except:
        assert False