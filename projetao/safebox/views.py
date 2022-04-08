from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Cliente, Assinatura, Plano, Ambiente
from .forms import AssinaturaForm, ClienteForm, ClienteLoginForm, AmbienteForm

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
        action_assinar = request.POST.get('assinar')
        action_visualizar = request.POST.get('visualizar')
        if action_desativar == 'Desativar Conta':
            context['data'].deactivate()
            context['data'].save()
            return redirect('login')

        if action_editar == 'Editar Conta':
            context['data'].reactivate()
            context['data'].save()
            return redirect('editar',context['data'].get_email())

        if action_visualizar == 'Visualizar Assinatura':
            return redirect('visualizar_assinatura',context['data'].get_email())

        if action_assinar == "Assinar plano":
            return redirect('assinar_plano',context['data'].get_email())

    return render(request, "cliente_detail_view.html", context)

def cliente_assinatura_view(request, email):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    assinaturas = Assinatura.objects.all()
    assinatura = assinaturas.filter(cliente_id=context['data'].id)

    if assinatura != None and len(assinatura) == 1:
        context['assinatura'] = assinatura[0]

    action_voltar = request.POST.get('voltar')
    action_trocar = request.POST.get('trocar_plano')
    action_remover = request.POST.get('remover_plano')

    if action_voltar == 'Voltar':
        return redirect('visualizar',email)

    if action_trocar == 'Trocar Plano':
        return redirect('trocar_assinatura', email)

    if action_remover == 'Remover Plano':
        #messages.info(request, "Assinatura desfeita com sucesso!")
        remover_assinatura(request, email)
        return redirect('visualizar', email)

    return render(request, "cliente_assinatura_view.html", context)

def remover_assinatura(request, email):
    cliente = Cliente.objects.get(email=email)
    assinaturas = Assinatura.objects.all()
    assinatura = assinaturas.filter(cliente_id=cliente.id)

    flag_assinatura_existente = False
    if (assinatura != None and len(assinatura)):
        flag_assinatura_existente = True

    if flag_assinatura_existente:
        assinatura[0].delete()

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
                if usuario.get_active() == False:
                    context['message'] = "Esse perfil de usuário está desativado!"
                    context["form"] = form
                    return render(request, "cliente_login_view.html", context)
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

def assinatura_create_view(request, email):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    assinaturas = Assinatura.objects.all()
    assinatura = assinaturas.filter(cliente_id=context['data'].id)

    flag_assinatura_existente = False
    if (assinatura != None) and (len(assinatura) != 0):
        flag_assinatura_existente = True

    form = AssinaturaForm(request.POST or None, initial={"cliente_id":context['data'].id})
    if form.is_valid() and not flag_assinatura_existente:
        form.save()
        return redirect('visualizar',email)

    planos = Plano.objects.all()
    context['form'] = form
    context['planos'] = planos

    return render(request, "assinatura_create_view.html", context)


def assinatura_trocar_view(request, email):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    assinaturas = Assinatura.objects.all()
    assinatura = assinaturas.filter(cliente_id=context['data'].id)

    flag_assinatura_existente = False
    if (assinatura != None) and (len(assinatura) != 0):
        flag_assinatura_existente = True

    form = AssinaturaForm(request.POST or None, initial={"cliente_id": context['data'].id})
    if form.is_valid() and flag_assinatura_existente:
        assinatura.delete()
        form.save()
        return redirect('visualizar_assinatura', email)

    planos = Plano.objects.all()
    context['form'] = form
    context['planos'] = planos

    return render(request, "assinatura_trocar_plano.html", context)


def ambiente_list_view(request,email):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.filter(cliente_id=context['data'].id)
    context['ambientes'] =[]
    if ambiente != None and len(ambiente) != 0:
        context['ambientes']=ambiente

    action_criar =  request.POST.get('criar')
    if action_criar == 'Criar ambiente':
        return redirect('criar_ambiente',email)

    for amb in ambiente:
        action_criar = request.POST.get('visualizar' + str(amb.get_nome()))
        action_desativar = request.POST.get('desativar' + str(amb.get_nome()))
        if action_criar == 'Visualizar':
            return redirect('ambiente_atual', email, amb.get_nome())
        if action_desativar == 'Desativar':
            amb.deactivate()
            return redirect('ambientes', email)

    return render(request, "ambiente_list_view.html", context)

def ambiente_create_view(request,email):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.filter(cliente_id=context['data'].id)
    form = AmbienteForm(request.POST or None, initial={"cliente_id":context['data'].id})
    flag_amb_existente = False
    if (ambiente != None) and (ambiente != []):
        for amb in ambiente:
            if amb.get_nome() == form['nome'].value():
                flag_amb_existente = True
                break
    try:

        if form.is_valid() and not flag_amb_existente:
            form.save()
            return redirect('ambientes',email)
        elif(form.is_valid() and flag_amb_existente):
            raise ValidationError('errou')

    except ValidationError:
        messages.info(request, 'Ambiente com esse nome já existe')

    context['form'] = form
    return render(request, "ambiente_create_view.html", context)

def ambiente_view(request, email, nome):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.filter(cliente_id=context['data'].id, nome=nome)

    if ambiente != None and len(ambiente) != 0:
        for amb in ambiente:
            context['ambiente'] = amb
            break

    return render(request, "ambiente_view.html", context)

