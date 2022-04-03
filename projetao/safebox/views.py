from django.shortcuts import render, redirect, HttpResponse

from .models import Cliente
from .forms import ClienteForm, ClienteLoginForm

def index(request):
    return HttpResponse("Safe Box")

def home_view(request, email):
    context = {}
    context["data"] = Cliente.objects.get(email=email)
    if request.method == "POST":
        action_sair = request.POST.get('sair')
        if action_sair == 'Sair':
            return redirect('login')
        action_visualizar = request.POST.get('visualizar')
        if action_visualizar == "Visualizar Conta":
            return redirect('visualizar', email)
    return render(request, "home_view.html", context)

def cliente_create_view(request):
    context = {}
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = request.POST['email']
        return redirect('login')
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
            return redirect('login')

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

################## Cliente Login e session ##################################
def cliente_login_view(request):
    context = {}
    try:
        form = ClienteLoginForm(request.POST or None)
        if form.is_valid():
            email = request.POST["email"]
            senha = request.POST["senha"]
            usuario = Cliente.objects.get(email=email)

            if usuario is not None:
                usuario = autenticar(usuario, senha=senha)
                if usuario is not None:
                    request.session['id'] = usuario.id
                    cliente_id = request.session['id']
                    session_state = {'email': usuario.get_email(), 'id':cliente_id}
                    return redirect('home', email)
                else:
                    context['message'] = "Senha incorreta!"
        elif request.method == 'POST':
            action = request.POST.get('cadastrar')
            if action == 'Cadastrar-se':
                return redirect('cadastrar')

    except Cliente.DoesNotExist:
        context['message'] = "Não existe usuário com este email!"

    context["form"] = form
    return render(request, "cliente_login_view.html", context)

def autenticar(usuario, senha):
    if usuario.get_senha() == senha:
        return usuario
    else:
        return None

def sair(request):
    try:
        del request.session['id']
    except KeyError:
        pass

    return redirect('login')
###################################################################
