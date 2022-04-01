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

    def deactivate(self):
        self.active = False

    def reactivate(self):
        self.active = True