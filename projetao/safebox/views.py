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
        action_desativar = request.POST.get('desativar')
        action_editar = request.POST.get('editar')
        if action_desativar == 'Desativar Conta':
            context['data'].deactivate()
            context['data'].save()
            return redirect('cadastrar')

        if action_editar == 'Editar Conta':
            context['data'].reactivate()
            context['data'].save()
            return redirect('editar',context['data'].get_email())

    return render(request, "cliente_detail_view.html", context)

def cliente_edit_view(request, email):
    context = {}
    context["data"] = Cliente.objects.get(email=email)

    # pass the object as instance in form
    form = ClienteForm(request.POST or None, instance=context['data'])

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        email = request.POST['email']
        return redirect('visualizar',email)

    # add form dictionary to context
    context["form"] = form

    return render(request, "cliente_edit_view.html", context)


