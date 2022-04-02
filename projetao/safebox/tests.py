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

    def test_desactivate(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        cliente.deactivate()
        self.assertEqual(False, cliente.active)

    def test_reactivate(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        cliente.reactivate()
        self.assertEqual(True, cliente.active)

    def test_edit_nome(self):
        novo_nome = "Testadorzinho"
        cliente = Cliente.objects.get(cpf_cnpj="00000000000")
        cliente.set_nome(novo_nome)
        self.assertEqual(cliente.get_nome(), novo_nome)

    def test_edit_email(self):
        novo_email = "testadorzinho@gmail.com"
        cliente = Cliente.objects.get(cpf_cnpj="00000000000")
        cliente.set_email(novo_email)
        self.assertEqual(cliente.get_email(), novo_email)

    def test_edit_contato(self):
        novo_contato = "12345678912"
        cliente = Cliente.objects.get(cpf_cnpj="00000000000")
        cliente.set_contato(novo_contato)
        self.assertEqual(cliente.get_contato(), novo_contato)

    def test_edit_cpf_cnpj(self):
        novo_cpf_cnpj = "11111111112"
        cliente = Cliente.objects.get(cpf_cnpj="00000000000")
        cliente.set_cpf_cnpj(novo_cpf_cnpj)
        self.assertEqual(cliente.get_cpf_cnpj(), novo_cpf_cnpj)

    def test_edit_senha(self):
        nova_senha = "senhazinha"
        cliente = Cliente.objects.get(cpf_cnpj="00000000000")
        cliente.set_senha(nova_senha)
        self.assertEqual(cliente.get_senha(), nova_senha)