from datetime import datetime

from django.test import TestCase
from .models import Camera, Cliente, Plano, Assinatura, Ambiente, Alerta, BoundingBox
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

class PlanoTest(TestCase):
    def setUp(self):
        self.plano = Plano()
        self.plano.nome = "Básico"
        self.plano.valor = 50.00
        self.plano.relatorio = False
        self.plano.numero_cameras = 1
        self.plano.numero_boundingbox = 3
        self.plano.save()
        
    def tearDown(self):
        plano = Plano.objects.get(nome="Básico")
        Plano.delete(plano)

    def test_fields(self):
        record = Plano.objects.get(nome="Básico")
        self.assertEqual(self.plano,record)
    
class AssinaturaTest(TestCase):
    def setUp(self):
        self.assinatura = Assinatura()
        cliente = Cliente.objects.create(nome="testador",email="teste@gmail.com",contato="00000000000",cpf_cnpj="00000000000",senha="123456")
        plano = Plano.objects.create(nome="Básico", valor=50.00, relatorio =False, numero_cameras=1, numero_boundingbox=3)
        self.assinatura = Assinatura.objects.create(cliente_id = cliente, plano_id = plano, data_de_pagamento=None,pagamento_status=False)
        

    def tearDown(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        assinatura = Assinatura.objects.get(cliente_id=cliente.id)
        Assinatura.delete(assinatura)
        plano = Plano.objects.get(nome="Básico")
        Plano.delete(plano)
        cliente = Cliente.objects.get(email="teste@gmail.com")
        Cliente.delete(cliente)

    def test_fields(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        record = Assinatura.objects.get(cliente_id=cliente.id)
        self.assertEqual(self.assinatura,record)


    def test_edit_plano(self):
        novo_plano = Plano.objects.create(nome="Premium", valor=100.00, relatorio=True, numero_cameras=3, numero_boundingbox=9)
        cliente = Cliente.objects.get(email="teste@gmail.com")
        assinatura = Assinatura.objects.get(cliente_id=cliente.id)
        assinatura.set_plano_id(novo_plano)
        self.assertEqual(assinatura.get_plano_id(), novo_plano)

class AmbienteTest(TestCase):
    def setUp(self):
        self.ambiente = Ambiente()
        cliente = Cliente.objects.create(nome="testador",email="teste@gmail.com",contato="00000000000",cpf_cnpj="00000000000",senha="123456")
        self.ambiente = Ambiente.objects.create(cliente_id = cliente, nome = "Ambiente de teste", numero_cameras=0)

    def test_fields(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        record = Ambiente.objects.get(cliente_id=cliente.id)
        self.assertEqual(self.ambiente,record)

    def test_deactivate_ambiente(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        self.ambiente.deactivate()
        lista_ambientes = Ambiente.objects.filter(cliente_id=cliente, nome="Ambiente de teste")
        self.assertEqual(len(lista_ambientes), 0)

class CameraTest(TestCase):
    def setUp(self):
        ambiente = Ambiente()
        cliente = Cliente.objects.create(nome="testador",email="teste@gmail.com",contato="00000000000",cpf_cnpj="00000000000",senha="123456")
        ambiente = Ambiente.objects.create(cliente_id = cliente, nome = "Ambiente de teste", numero_cameras=0)
        self.camera = Camera()
        self.camera = Camera.objects.create(nome="camera teste", ip="10.0.0.0", ambiente_id = ambiente, usuario="admin", senha="admin", porta="8080")
    
    def test_fields(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        ambiente = Ambiente.objects.get(cliente_id=cliente.id)
        record = Camera.objects.get(ambiente_id=ambiente.id)
        self.assertEqual(record, self.camera)

    def test_delete_camera(self):
        camera_ip = self.camera.get_ip()
        self.camera.delete()

        with self.assertRaises(Camera.DoesNotExist):
            Camera.objects.get(ip=camera_ip)
            
    def test_Edit_Nome(self):
        cliente = Cliente.objects.get(email="teste@gmail.com")
        ambiente = Ambiente.objects.get(cliente_id=cliente.id)
        camera = Camera.objects.get(ambiente_id=ambiente.id)
        novo_nome = 'Cam_Teste'
        camera.set_nome(novo_nome)
        self.assertEqual(camera.get_nome(), novo_nome)

class AlertaTest(TestCase):
    def setUp(self):
        ambiente = Ambiente()
        cliente = Cliente.objects.create(nome="testador", email="teste@gmail.com", contato="00000000000",
                                         cpf_cnpj="00000000000", senha="123456")
        ambiente = Ambiente.objects.create(cliente_id=cliente, nome="Ambiente de teste", numero_cameras=0)

        self.camera = Camera()
        self.camera = Camera.objects.create(nome="camera teste", ip="10.0.0.0", ambiente_id=ambiente, usuario="admin",
                                            senha="admin", porta="8080")
        bounding_box = BoundingBox()
        bounding_box.x1 = 20
        bounding_box.y1 = 20
        bounding_box.x2 = 200
        bounding_box.y2 = 200
        bounding_box.num_min_pessoas = 1
        bounding_box.num_max_pessoas = 2
        bounding_box.horario_inicial = datetime.strptime('06:00:00', '%H:%M:%S').time()
        bounding_box.horario_final = datetime.strptime('23:00:00', '%H:%M:%S').time()
        bounding_box.cor = 345673
        bounding_box.camera_ip = self.camera
        bounding_box.save()

        self.alerta = Alerta()
        self.alerta.bounding_box_id = BoundingBox.objects.last()
        self.alerta.data = datetime.strptime('22/5/05', '%y/%m/%d').date()
        self.alerta.hora = datetime.strptime('08:00:00', '%H:%M:%S').time()
        self.alerta.tipo = 'min'
        self.alerta.save()

    def test_create_alert(self):
        alerta = Alerta.objects.last()
        self.assertEqual(self.alerta, alerta)


