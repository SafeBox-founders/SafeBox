from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class ClienteLoginForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.EmailInput)
    senha = forms.CharField(max_length=12, widget=forms.PasswordInput)
