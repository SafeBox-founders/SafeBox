from django.shortcuts import render, redirect, HttpResponse

from .models import Cliente
from .forms import ClienteForm

def index(request):
    return HttpResponse("Safe Box")

def cliente_create_view(request):
    context = {}
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = request.POST['email']
        return redirect('visualizar',email)
    context["form"] = form
    return render(request, "cliente_create_view.html", context)

def cliente_detail_view(request, email):
    context = {}
    context["data"] = Cliente.objects.get(email=email)
    if request.method == 'POST':
        action = request.POST.get('desativar')
        if action == 'Desativar Conta':
            context['data'].deactivate()
            context['data'].save()

        return redirect('cadastrar')

    return render(request, "cliente_detail_view.html", context)

