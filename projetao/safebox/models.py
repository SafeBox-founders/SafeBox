from asyncio.windows_events import NULL
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