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
    choice.send_keys("#000000")

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

@given("I created a bounding box")
def step_impl(context):
    context.execute_steps(u"""
        Given I am at an Camera view
        When I fill the create bounding box fields
        And I click on criar bounding box
        Then I can see the created bounding box
        """)
    #sleep(120)

@Given("I click on editar box")
def step_impl(context):
    boxes = BoundingBox.objects.all()

    btn_ver = context.browser.find_element_by_name("verbox" + str(boxes.last().id))
    btn_ver.click()

    btn_editar = context.browser.find_element_by_id("editarBox"+str(boxes.last().id))
    btn_editar.click()

@Given("I fil the editar box fields")
def step_impl(context):
    choice = context.browser.find_element_by_id("id_x1")
    choice.send_keys(20)
    choice = context.browser.find_element_by_id("id_x2")
    choice.send_keys(20)
    choice = context.browser.find_element_by_id("id_y1")
    choice.send_keys(155)
    choice = context.browser.find_element_by_id("id_y2")
    choice.send_keys(155)
    choice = context.browser.find_element_by_id("id_num_max_pessoas")
    choice.send_keys(2)
    choice = context.browser.find_element_by_id("id_num_min_pessoas")
    choice.send_keys(5)
    choice = context.browser.find_element_by_id("id_horario_inicial")
    choice.send_keys("09:10")
    choice = context.browser.find_element_by_id("id_horario_final")
    choice.send_keys("10:30")
    choice = context.browser.find_element_by_id("id_cor")
    choice.send_keys("#000000")

@When("I click on confirmar edicao of box")
def step_impl(context):
    boxes = BoundingBox.objects.all()
    btn_confirm = context.browser.find_element_by_name("editarBoundingBox"+str(boxes.last().id))
    btn_confirm.click()

@Then("I see that the box was edited")
def step_impl(context):
    boxes = BoundingBox.objects.all()
    box = boxes.last()
    assert str(box.x1) == str(20)
    assert str(box.x2) == str(20)
    assert str(box.y1) == str(155)
    assert str(box.y2) == str(155)
    assert str(box.num_max_pessoas) == str(2)
    assert str(box.num_min_pessoas) == str(5)
    assert str(box.horario_inicial) == str("09:10:00")
    assert str(box.horario_final) == str("10:30:00")
    assert str(box.cor) == str("#000000")

@Given("I do not fill all box fields")
def step_impl(context):
    choice = context.browser.find_element_by_id("id_x1")
    choice.send_keys(20)
    choice = context.browser.find_element_by_id("id_x2")
    choice.send_keys(20)

@Then("I can see that the box was not edited")
def step_impl(context):
    boxes = BoundingBox.objects.all()
    box = boxes.last()
    assert str(box.x1) != str(20)