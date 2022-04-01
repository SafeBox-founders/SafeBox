import os
from time import sleep
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","projetao.settings")
django.setup()

from behave import fixture, use_fixture
from safebox.models import Cliente
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
from selenium import webdriver

class BaseTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        Cliente.objects.create(name="Testador", email="cliente@gmail.com", contato="00000000000", cpf_cnpj = "121012121", senha="123456")
        super(BaseTestCase,cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        Cliente.objects.all().delete()
        super(BaseTestCase,cls).tearDownClass()

@fixture
def django_test_case(context):
    context.test_case = BaseTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    context.selenium.quit()
    del context.test_case

@fixture
def django_test_runner(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


def before_all(context):
    context.browser = webdriver.Chrome()
    use_fixture(django_test_runner, context)

def before_scenario(context, scenario):
    use_fixture(django_test_case, context)

@fixture
def browser_chrome(context):
    context.browser = webdriver.Chrome()
    yield context.browser
    context.browser.quit()

def after_all(context):
    cliente = Cliente.objects.all()
    cliente.delete(all)