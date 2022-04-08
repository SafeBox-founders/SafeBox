import os
import sys
import pdb
from datetime import datetime

from time import sleep
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","projetao.settings")
django.setup()
sys.path.append("/home/battist/PycharmProjects/SafeBox")
from os import path
from behave import *
from pandas import options
from selenium import webdriver
from safebox.models import Cliente, Assinatura

use_step_matcher("re")

@given("I am on the Profile View")
def step_impl(context):
    context.execute_steps(u"""
        given I am registered user
        and I access the profile view
        """)

@when("I click on the Assinar plano button")
def step_impl(context):
    button = context.browser.find_element_by_name("assinar")
    button.click()

@When("I chose my plan")
def step_impl(context):
    choice = context.browser.find_element_by_name("plano_id")
    choice.send_keys("Básico")

@When("I click on the Assinar button")
def step_impl(context):

    button = context.browser.find_element_by_name("assinar")
    button.click()

@Then("I assigned my plan")
def step_impl(context):
    global atts_dictionary_plano

    assinaturas = Assinatura.objects.all()
    ultima_assinatura = assinaturas.latest('data_de_pagamento')
    atts_dictionary_plano = {'Nome do Plano': str(ultima_assinatura.plano_id),
                       #'Data de Pagamento': str(ultima_assinatura.data_de_pagamento),
                       'Status do Pagamento': str(ultima_assinatura.pagamento_status)}

    assert assinaturas.filter(plano_id=1) != []

@Given("I have a signature")
def step_impl(context):
    context.execute_steps(u"""
        When I click on the Assinar plano button
        And I chose my plan 
        And I click on the Assinar button
        Then I assigned my plan
        """)

@When("I click on the Visualizar Assinatura button")
def step_impl(context):
    button = context.browser.find_element_by_name("visualizar")
    button.click()

@Then("I go to my signature view")
def step_impl(context):
    assert context.browser.title=="Assinatura"

@Then("I can see my current signature")
def step_impl(context):
    div = context.browser.find_element_by_id("div_client_assinatura_info")
    textos = (div.text).split("\n")
    atts_dictionary_novo = {}
    for i in range(len(textos)):
        if (textos[i] != "" and (":" in textos[i])):
            atts_dictionary_novo[textos[i].split(": ")[0]] = textos[i].split(": ")[1]
    atts_dictionary_novo.pop('Data de Pagamento')

    for key in atts_dictionary_novo.keys():
        assert atts_dictionary_novo[key] == atts_dictionary_plano[key]




@Then('I click on Trocar Plano')
def step_impl(context):
    button = context.browser.find_element_by_name("trocar_plano")
    button.click()


@Then('I chose my new plan')
def step_impl(context):
    choice = context.browser.find_element_by_name("plano_id")
    choice.send_keys("Premium")

@Then('I click on Mudar de plano')
def step_impl(context):
    button = context.browser.find_element_by_name("trocar")
    button.click()

@Then('I can see my new signature')
def step_impl(context):
    assert context.browser.title=="Assinatura"





