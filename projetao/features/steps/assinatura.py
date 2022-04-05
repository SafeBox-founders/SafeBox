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
from safebox.models import Cliente, Assinatura

use_step_matcher("re")

@given("I am on the Profile View")
def step_impl(context):
    context.execute_steps(u"""
        given I am registered user
        and I access the profile view
        when I click on Editar Conta
        and I fill all fields
        and I click on Editar
        then I go to my profile view
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
    assinatura = Assinatura.objects.all()
    assert assinatura.filter(plano_id=1) != []
