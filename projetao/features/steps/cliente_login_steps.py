import os
import sys
import pdb
import time
from django.utils import timezone

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
use_step_matcher("re")

@given('Eu sou um usuario cadastrado')
def step_impl(context):
    context.execute_steps(u"""
        given I am on the Cadastrar Cliente View
        and I fill all fields
        when I click on the Submit button
        then I create my profile 
        and I go to Login page
        """)

@given('Eu estou na tela de login')
def step_impl(context):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/google-chrome-stable'
    driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    context.browser = driver
    context.browser.get("http://127.0.0.1:8000/")
    #context.browser.title == "Login"

@given('Eu preencho o campo email e senha')
def step_impl(context):
    email = context.browser.find_element_by_name("email")
    senha = context.browser.find_element_by_name("senha")
    cliente = Cliente.objects.last()

    email.send_keys(cliente.get_email())
    senha.send_keys(cliente.get_senha())

@when('Eu pressiono o botao "Logar"')
def step_impl(context):
    button_logar = context.browser.find_element_by_name("logar")
    button_logar.click()

@then('Eu vejo que estou logado')
def step_impl(context):
    assert context.browser.title == "SafeBox"

@given('Eu preencho o campo email e senha com dados nao cadastrados')
def step_impl(context):
    email = context.browser.find_element_by_name("email")
    senha = context.browser.find_element_by_name("senha")

    email.send_keys("rogerio@email.com")
    senha.send_keys("123456")

@then('Eu vejo a mensagem de erro')
def step_impl(context):
    alert = context.browser.switch_to.alert
    texto = alert.text

    alert.accept()

    assert texto == "Não existe usuário com este email!"

@given(u'Eu estou logado')
def step_impl(context):
    context.execute_steps(u"""
        given Eu sou um usuario cadastrado
        and Eu estou na tela de login
        and Eu preencho o campo email e senha
        when Eu pressiono o botao "Logar"
        then Eu vejo que estou logado""")


@given('Eu estou na tela de home')
def step_impl(context):
    title = context.browser.title
    assert title == "SafeBox"

@when('Eu pressiono o botao sair')
def step_impl(context):
    button_sair = context.browser.find_element_by_name("sair")
    button_sair.click()

@when('Eu estou na tela de login')
def step_impl(context):
    title = context.browser.title
    assert title == "Login"