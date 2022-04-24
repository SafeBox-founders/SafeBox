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
from safebox.models import Cliente, Ambiente, Camera

use_step_matcher("re")

@given("I am at an Ambiente view")
def step_impl(context):
    context.execute_steps(u"""
        given I am on ambientes list view
        and There is a registered ambiente
        when I click on view a existing ambiente
        then I go the existing ambiente detail page
        """)

@when("I click on Adicionar nova câmera")
def step_impl(context):
    button = context.browser.find_element_by_name("addcam")
    button.click()

@when("I fill the criar camera fields")
def step_impl(context):
    choice = context.browser.find_element_by_name("nome")
    choice.send_keys("teste")
    camera = Camera.objects.all()
    global ip
    ip = str(len(camera))
    choice = context.browser.find_element_by_name("ip")
    choice.send_keys(ip)
    choice = context.browser.find_element_by_name("usuario")
    choice.send_keys("admin")
    choice = context.browser.find_element_by_name("senha")
    choice.send_keys("9621")
    choice = context.browser.find_element_by_name("porta")
    choice.send_keys("80")

@when("I click on the criar camera button")
def step_impl(context):
    button = context.browser.find_element_by_name("criar")
    button.click()

@then("I go back to an existing ambiente detail page")
def step_impl(context):
    nome_ambiente = str(context.browser.session_id)
    assert context.browser.title == nome_ambiente

@then("I created a camera")
def step_impl(context):
    camera = Camera.objects.all()
    assert len(camera.filter(nome="teste"))>0

@given("I have a created camera")
def step_impl(context):
    context.execute_steps(u"""
        given I am at an Ambiente view
        when I click on Adicionar nova câmera 
        and I fill the criar camera fields
        and I click on the criar button
        then I go the existing ambiente detail page
        and I created a camera
        """)

@given("I click on visualizar camera")
@when("I click on visualizar camera")
def step_impl(context):
    button = context.browser.find_element_by_name("visualizar"+str(ip))
    button.click()

@then("I go to the camera view")
def step_impl(context):
    assert context.browser.title == str(ip)

@given("I click on remover camera")
def step_impl(context):
    remove = context.browser.find_element_by_name("remover"+str(ip))
    remove.click()

@given("I can see the message confirm for remover camera")
def step_impl(context):
    confirm = context.browser.switch_to.alert
    texto = confirm.text
    assert texto == "Essa câmera será removida! Deseja continuar?"

@When("I click on confirm button \'OK\' to remover camera")
def step_impl(context):
    confirm = context.browser.switch_to.alert
    confirm.accept()