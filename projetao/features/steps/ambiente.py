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
from safebox.models import Cliente, Ambiente

use_step_matcher("re")

@given("I am on the Home View")
def step_impl(context):
    context.execute_steps(u"""
        given I am registered user
        """)
@when("I click on Gerenciar câmeras")
def step_impl(context):
    button = context.browser.find_element_by_name("gerenciar_câmeras")
    button.click()

@when("I click on the criar ambiente button")
def step_impl(context):
    button = context.browser.find_element_by_name("criar")
    button.click()

@when("I fill the criar ambiente fields")
def step_impl(context):
    choice = context.browser.find_element_by_name("nome")
    choice.send_keys("Ambiente de teste")

@when("I click on the criar button")
def step_impl(context):
    button = context.browser.find_element_by_name("criar")
    button.click()

@then("I go to Criar ambiente view")
def step_impl(context):
    assert context.browser.title == "Criar Ambiente"

@then("I created a ambiente")
def step_impl(context):
    ambiente = Ambiente.objects.all()
    assert ambiente.filter(nome="Ambiente de teste")  != []


#=====================================================================

@Given("I am on ambientes list view")
def step_impl(context):
    context.execute_steps(u"""
        given I am on the Home View
        when I click on Gerenciar câmeras 
        and I click on the criar ambiente button
        and I fill the criar ambiente fields
        and I click on the criar button
        then I go to Criar ambiente view
        """)

@Given("There is a registered ambiente")
def step_impl(context):
    ambiente = Ambiente.objects.all()
    assert ambiente.filter(nome="Ambiente de teste")  != []

@When("I click on view a existing ambiente")
def step_impl(context):
    button = context.browser.find_element_by_name("visualizarAmbiente de teste")
    button.click()

@Then("I go the existing ambiente detail page")
def step_impl(context):
    assert context.browser.find_element_by_name("Ambiente de teste")



