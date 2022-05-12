import os
import sys

from time import sleep
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","projetao.settings")
django.setup()
sys.path.append("/home/battist/PycharmProjects/SafeBox")
from behave import *
from pathlib import Path

use_step_matcher("re")

@given(u'I am on Relatorio view')
def step_impl(context):
    context.execute_steps(u"""
        given I have a created camera
        and I am on the Home View
    """)

@given(u'I click on Relatorios')
def step_impl(context):
    opt_relatorios = context.browser.find_element_by_name("relatorios")
    opt_relatorios.click()

@given(u'I click on Gerar Relatorio')
def step_impl(context):
    btn_gerar = context.browser.find_element_by_name("gerarRelatorio")
    btn_gerar.click()

@given(u'I insert the initial and final dates')
def step_impl(context):
    initial = context.browser.find_element_by_name("data_inicial")
    initial.send_keys("01/05/2022")
    final = context.browser.find_element_by_name("data_final")
    final.send_keys("31/05/2022")

@when(u'I click on Criar Relatorio')
def step_impl(context):
    btn_criar = context.browser.find_element_by_name("criarRelatorio")
    btn_criar.click()

@then(u'I see that the report was created')
def step_impl(context):
    title = context.browser.title
    assert title == "Relatórios Visualizar"

@given(u'I created a relatorio')
def step_impl(context):
    context.execute_steps(u"""
        given I am on Relatorio view
        and I click on Relatorios
        and I click on Gerar Relatorio
        and I insert the initial and final dates
        when I click on Criar Relatorio
        then I see that the report was created
    """)

@when(u'I click on Exportar Relatorio')
def step_impl(context):
    btn_export = context.browser.find_element_by_name("exportarRelatorio")
    btn_export.click()

@then(u'I see that the report was downloaded')
def step_impl(context):
    #01/05/2022
    #31/05/2022
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
    print("Download path", path_to_download_folder)
    assert os.path.isfile(path_to_download_folder.replace("'\'", "/")+"/relatorio2022-05-01----2022-05-31.pdf") is True

@when(u'I click on Historico of the report')
def step_impl(context):
    btn_hist = context.browser.find_element_by_name("visualizarHistorico")
    btn_hist.click()

@then(u'I see the report history')
def step_impl(context):
    title = context.browser.title
    assert title == "Histórico de relatórios"
