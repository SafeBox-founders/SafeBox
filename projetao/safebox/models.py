from django.db import models
from django.urls import reverse

class Cliente(models.Model):
    nome = models.CharField(max_length=255,null=False)
    email = models.EmailField(max_length=255,null=False,unique=True)
    contato = models.CharField(max_length=11,null=False)
    cpf_cnpj = models.CharField(max_length=11,null=False,unique=True)
    senha = models.CharField(max_length=12,null=False)
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('visualizar',kwargs={"str":self.email})

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_contato(self):
        return self.contato

    def get_cpf_cnpj(self):
        return self.cpf_cnpj

    def get_senha(self):
        return self.senha

    def set_nome(self, nome_p):
        self.nome = nome_p

    def set_email(self, email_p):
        self.email = email_p

    def set_contato(self, contato_p):
        self.contato = contato_p

    def set_cpf_cnpj(self, cpf_cnpj_p):
        self.cpf_cnpj = cpf_cnpj_p

    def set_senha(self, senha_p):
        self.senha = senha_p

    def deactivate(self):
        self.active = False

    def reactivate(self):
        self.active = True

    def get_active(self):
        return self.active

class Plano(models.Model):
    nome = models.CharField(max_length=255,null=False, unique=True)
    valor = models.FloatField(null=False)
    relatorio = models.BooleanField(null=False)
    numero_cameras = models.IntegerField(null=False)
    numero_boundingbox = models.IntegerField(null=False)

    def __str__(self):
        return self.nome

class Assinatura(models.Model):
    cliente_id = models.ForeignKey(Cliente, to_field="id", on_delete=models.CASCADE)
    plano_id = models.ForeignKey(Plano, to_field="id",on_delete=models.CASCADE)
    data_de_pagamento = models.DateTimeField(auto_now_add=True)
    pagamento_status = models.BooleanField(null=False, default=False)

    def get_cliente_id(self):
        return self.cliente_id

    def get_plano_id(self):
        return self.plano_id

    def get_data_de_pagamento(self):
        return self.data_de_pagamento

    def get_pagamento_status(self):
        return self.pagamento_status

    def set_plano_id(self, novo_plano_id):
        self.plano_id = novo_plano_id


class Ambiente(models.Model):
    cliente_id = models.ForeignKey(Cliente, to_field="id", on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, null=False)
    numero_cameras = models.IntegerField(null=False,default=0)

    def __str__(self):
        return self.nome

    def get_cliente_id(self):
        return self.cliente_id

    def get_nome(self):
        return  self.nome

    def get_numero_cameras(self):
        return self.numero_cameras

    def set_nome(self, novo_nome):
        self.nome = novo_nome

    def deactivate(self):
        self.delete()

class Camera(models.Model):
    ip = models.CharField(max_length=255, null=False, unique=True)
    nome = models.CharField(max_length=255, null=False)
    num_boundingbox = models.IntegerField(null=False,default=0)
    ambiente_id = models.ForeignKey(Ambiente, to_field="id", on_delete=models.CASCADE)
    usuario = models.CharField(max_length=255, null=False)
    senha = models.CharField(max_length=255, null=False)
    porta = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return self.nome
    
    def get_ip(self):
        return self.ip

    def get_nome(self):
        return self.nome

    def set_nome(self, novo_nome):
        self.nome = novo_nome

class BoundingBox(models.Model):
    camera_ip = models.ForeignKey(Camera, to_field="ip", on_delete=models.CASCADE)
    x1 = models.IntegerField(null=False)
    x2 = models.IntegerField(null=False)
    y1 = models.IntegerField(null=False)
    y2 = models.IntegerField(null=False)
    num_max_pessoas = models.IntegerField(null=False)
    num_min_pessoas = models.IntegerField(null=False)
    horario_inicial = models.TimeField(null=False)
    horario_final = models.TimeField(null=False)
    cor = models.IntegerField(null=False)

    def to_dict(self):
        dict = {"y1": str(self.y1), "x1": str(self.x1), "y2": str(self.y2), "x2": str(self.x2),
                "start": str(self.horario_inicial), "end": str(self.horario_final), "min": str(self.num_min_pessoas),
                "max": str(self.num_max_pessoas)}
        return dict

class Alerta(models.Model):
    bounding_box_id = models.ForeignKey(BoundingBox, to_field='id', on_delete=models.CASCADE)
    data = models.DateField(null=False)
    hora = models.TimeField(null=False)
    tipo = models.TextField(null=False)
