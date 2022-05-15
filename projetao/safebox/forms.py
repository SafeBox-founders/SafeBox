from unicodedata import name
from django import forms
from .models import Ambiente, Assinatura, Camera, Cliente, Plano, BoundingBox, Relatorio
from django.core.exceptions import ValidationError

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "contato", "cpf_cnpj", "senha"]
        widgets = {
            "cpf_cnpj" : forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Digite somente números'}),
            "contato" : forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Digite somente números'})
        }

    def clean_contato(self):
        contato = self.cleaned_data['contato']
        min_length = 8
        max_length = 11

        if len(contato) < min_length or len(contato) > max_length:
            raise ValidationError("Contato residencial ou celular deve ter entre %s e %s números!" %(min_length, max_length))
        else:
            return contato

    def clean_cpf_cnpj(self):
        value = self.cleaned_data['cpf_cnpj']
        min_length = 11
        if len(str(value)) < min_length:
            raise ValidationError(
                "CPF ou CNPJ deve ter no mínimo 11 caracteres! '%s' tem apenas %s." %(value, len(value)))
        else:
            return value

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

CHOICES = [
    ("000000","Preto"),
    ("FF0000","Azul"),
    ("00FF00","Verde"),
    ("F020A0","Roxo"),
    ("CBC0FF","Rosa"),
    ("0000FF","Vermelho"),
    ("00A5FF","Laranja"),
    ("00FFFF","Amarelo"),
    ("FFFFFF","Branco")]

class BoundingBoxForm(forms.ModelForm):
    class Meta:
        model = BoundingBox
        fields = ["camera_ip","x1","y1","x2","y2","num_max_pessoas","num_min_pessoas","horario_inicial","horario_final"]
        widgets = {"camera_ip": forms.HiddenInput()}

    cor = forms.ChoiceField(choices=CHOICES, widget=forms.Select(), required=True)

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ["cliente_id", "data_inicial", "data_final"]
        widgets = {"cliente_id": forms.HiddenInput()}