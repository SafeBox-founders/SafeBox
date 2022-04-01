from django.test import TestCase
from .models import Cliente
import unittest
from django.urls import reverse

#testes de unidade

class ClienteTest(TestCase):

    def setUp(self):
        self.cliente = Cliente()
        self.cliente.nome = "Testador"
        self.cliente.email = "teste@gmail.com"
        self.cliente.contato = "00000000000"
        self.cliente.cpf_cnpj = "00000000000"
        self.cliente.senha = "123456"
        self.cliente.save()

    def tearDown(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        Cliente.delete(cliente)

    def test_fields(self):
        record = Cliente.objects.get(email="teste@gmail.com")
        self.assertEqual(self.cliente,record)
    
    def test_get_absolute_url(self):
        record = Cliente.objects.get(email="teste@gmail.com")
        testurl = reverse('visualizar',args=[record.email])
        url = reverse('visualizar', args=[self.cliente.email])
        self.assertEqual(url,testurl)