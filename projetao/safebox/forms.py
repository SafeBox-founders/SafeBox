from unicodedata import name
from django import forms
from .models import Ambiente, Assinatura, Camera, Cliente, Plano

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "contato", "cpf_cnpj", "senha"]

class ClienteLoginForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.EmailInput)
    senha = forms.CharField(max_length=12, widget=forms.PasswordInput)

class AssinaturaForm(forms.ModelForm):
    class Meta:
        model = Assinatura
        fields = ['plano_id','cliente_id']
        widgets = {'cliente_id': forms.HiddenInput()}
    def __init__(self,*args,**kwargs):
        super(AssinaturaForm,self).__init__(*args,**kwargs)
        self.fields["plano_id"].queryset = Plano.objects.all()

class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = ['nome','cliente_id','numero_cameras']
        widgets = {'cliente_id':forms.HiddenInput(), 'numero_cameras':forms.HiddenInput()}

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ["ip", "nome", "usuario", "senha", "porta", "ambiente_id", "num_boundingbox"]
        widgets = {"ambiente_id":forms.HiddenInput(), "num_boundingbox":forms.HiddenInput()}