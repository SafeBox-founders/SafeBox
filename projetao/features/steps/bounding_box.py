import os
import sys
import pdb

from time import sleep
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","projetao.settings")
django.setup()
sys.path.append("/Documentos/SafeBox")
from os import path
from behave import *
from pandas import options
from selenium import webdriver
from safebox.models import Cliente, Ambiente, Camera, BoundingBox

use_step_matcher("re")

@given("I am at an Camera view")
def step_impl(context):
    context.execute_steps(u"""
        Given I have a created camera
        When I click on visualizar camera
        Then I go to the camera view
        """)

@When("I fill the create bounding box fields")
def step_impl(context):
    button = context.browser.find_element_by_name("nova")
    button.click()
    choice = context.browser.find_element_by_name("x1")
    choice.send_keys(15)
    choice = context.browser.find_element_by_name("x2")
    choice.send_keys(15)
    choice = context.browser.find_element_by_name("y1")
    choice.send_keys(150)
    choice = context.browser.find_element_by_name("y2")
    choice.send_keys(150)
    choice = context.browser.find_element_by_name("num_max_pessoas")
    choice.send_keys(1)
    choice = context.browser.find_element_by_name("num_min_pessoas")
    choice.send_keys(2)
    choice = context.browser.find_element_by_name("horario_inicial")
    choice.send_keys("09:00")
    choice = context.browser.find_element_by_name("horario_final")
    choice.send_keys("10:00")
    choice = context.browser.find_element_by_name("cor")
    choice.send_keys(111111)

@When("I click on criar bounding box")
def step_impl(context):
    global boundingBoxes
    boundingBoxes = len(BoundingBox.objects.all())
    button = context.browser.find_element_by_name("criarBoundingBox")
    button.click()

@Then("I can see the created bounding box")
def step_impl(context):
    boxes = len(BoundingBox.objects.all())
    assert boxes == boundingBoxes+1



@Then("I can see the bounding box information")
def step_impl(context):
    boxes = BoundingBox.objects.all()
    box = context.browser.find_element_by_name("verbox"+str(boxes[len(boxes)-1].id))
    assert box != None
