import json
import os

from django.core import serializers
from os import name
from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib import messages
from .models import Camera, Cliente, Assinatura, Plano, Ambiente, BoundingBox
from .forms import AssinaturaForm, CameraForm, ClienteForm, ClienteLoginForm, AmbienteForm, BoundingBoxForm
import cv2
from django.http import StreamingHttpResponse

width = 0
height = 0

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

def payments(request, email, id):
    context = {}
    assinatura = Assinatura.objects.all()
    assinatura = assinatura.filter(id=id)
    if assinatura != None and len(assinatura) != 0:
        plano = Plano.objects.all()
        plano = plano.filter(nome=assinatura[0].plano_id)
        if plano != None and len(plano) != 0:
            context['plano_valor'] = plano[0].valor

    variavel = request.POST.get('voltar')
    if variavel == 'Voltar':
        return redirect('visualizar', email)


    context['data'] = Cliente.objects.get(email=email)

    return render(request, 'payments.html', context)

def assinatura_create_view(request, email):
    context = {}
    tmp = {}
    context['data'] = Cliente.objects.get(email=email)
    assinaturas = Assinatura.objects.all()
    assinatura = assinaturas.filter(cliente_id=context['data'].id)

    flag_assinatura_existente = False
    if (assinatura != None) and (len(assinatura) != 0):
        flag_assinatura_existente = True

    form = AssinaturaForm(request.POST or None, initial={"cliente_id":context['data'].id})
    if form.is_valid() and not flag_assinatura_existente:
        plano_id_temp = form['plano_id'].value()
        plano = Plano.objects.all()
        plano = plano.filter(id=plano_id_temp)

        if plano != None and len(plano) > 0:
            context['valor_plano'] = plano[0].valor
            #tmp['valor_plano'] = plano[0].valor
            tmp['email'] = email
            form.save()
            assinatura = Assinatura.objects.all()
            assinatura = assinatura.filter(cliente_id=context['data'].id)
            if assinatura != None and len(assinatura) != 0:
                tmp['id'] = assinatura[0].id
                return redirect('payments', email, assinatura[0].id)

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
        action_editar = request.GET.get('editar' + str(amb.get_nome()))
        if action_criar == 'Visualizar':
            return redirect('ambiente_atual', email, amb.get_nome())
        if action_desativar == 'Desativar':
            amb.deactivate()
            return redirect('ambientes', email)
        if action_editar == "Editar":
            return redirect("editar_ambiente", email, amb.get_nome())

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
    cameras = Camera.objects.all()
    camera = cameras.filter(ambiente_id = ambiente[0].id)
    context['cameras'] = []
    if camera != None and len(camera) != 0:
        context['cameras'] = camera

    action_criar =  request.POST.get('addcam')
    if action_criar == 'Adicionar nova câmera':
        return redirect('criar_camera',email, nome)

    for cam in camera:
        action_criar = request.POST.get('visualizar' + str(cam.get_ip()))
        action_remover = request.POST.get('remover' + str(cam.get_ip()))
        if action_criar == 'Visualizar':
            return redirect('camera_atual', email, nome, cam.get_ip())
        if action_remover == "Remover":
            remover_camera(email, nome, cam.get_ip())
            messages.success(request, "Câmera", cam.get_ip(), " removida com sucesso.")
            return redirect('ambiente_atual', email, nome)


        action_edit = request.POST.get('editar' + str(cam.get_ip()))
        if action_edit == 'Editar':
            return redirect('camera_edit', email, nome, cam.get_ip())

    if ambiente != None and len(ambiente) != 0:
        for amb in ambiente:
            context['ambiente'] = amb
            break

    if context['ambiente'] != None:
        action_edit = request.GET.get('editar_ambiente')
        if action_edit == "Editar Ambiente":
            return redirect("editar_ambiente", email, context['ambiente'].get_nome())

    return render(request, "ambiente_view.html", context)

def ambiente_edit_view(request, email, nome):
    action_cancelar = request.GET.get('cancelar')
    if action_cancelar == "Cancelar":
        return redirect("ambientes", email)

    context = {}
    context['data'] = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.filter(cliente_id=context['data'].id, nome=nome)

    form = AmbienteForm(request.POST or None, initial={"cliente_id": context['data'].id, "numero_cameras": ambiente[0].get_numero_cameras()})

    flag_amb_existente = False
    if (ambiente != None) and (ambiente != []):
        for amb in ambiente:
            if amb.get_nome() == form['nome'].value():
                flag_amb_existente = True
                break

    try:
        if form.is_valid() and not flag_amb_existente:
            ambiente[0].set_nome(form['nome'].value())
            ambiente[0].save()
            return redirect('ambientes', email)
        elif (form.is_valid() and flag_amb_existente):
            raise ValidationError('errou')

    except ValidationError:
        messages.info(request, 'Ambiente com esse nome já existe ou o nome não está sendo modificado!')

    context['form'] = form
    context['nome_in_edit'] = nome
    return render(request, "ambiente_edit_view.html", context)

def camera_view(request, email, nome, ip):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.get(cliente_id=context['data'].id, nome=nome)
    cameras = Camera.objects.all()
    camera = cameras.filter(ambiente_id = ambiente.id, ip = ip)
    context['ambiente_name'] = nome
    context['camera'] = camera[0]
    bounding_box_form = BoundingBoxForm(request.POST or None, initial={"camera_ip": ip})
    context['form_bounding_box'] = bounding_box_form
    bounding_boxes = BoundingBox.objects.all().filter(camera_ip=ip)
    context['bounding_boxes'] = bounding_boxes

    if camera != None and len(camera) != 0:
        for cam in camera:
            context['camera'] = cam
            action_remover = request.POST.get('remover' + str(cam.get_ip()))
            action_criar_bounding_box = request.POST.get('criarBoundingBox')
            if action_remover == "Remover":
                remover_camera(email, nome, cam.get_ip())
                messages.success(request, "Câmera", cam.get_ip(), " removida com sucesso.")
                return redirect('ambiente_atual',email, nome)

            global width
            global height
            #width = 810
            #height = 540
            if action_criar_bounding_box == "Criar Bounding Box":
                if (bounding_box_form.is_valid()):
                    if (0 > int(bounding_box_form['x1'].value()) or int(bounding_box_form['x1'].value()) > width):
                        messages.info(request,
                                      "Valor de X1 negativo ou superior ao tamanho da imagem, valor máximo:" + str(
                                          width))
                    elif (0 > int(bounding_box_form['y1'].value()) or int(bounding_box_form['y1'].value()) > height):
                        messages.info(request,
                                      "Valor de Y1 negativo ou superior ao tamanho da imagem, valor máximo:" + str(
                                          height))
                    elif (0 > int(bounding_box_form['x2'].value()) or int(bounding_box_form['x2'].value()) > width):
                        messages.info(request,
                                      "Valor de X2 negativo ou superior ao tamanho da imagem, valor máximo:" + str(
                                          width))
                    elif (0 > int(bounding_box_form['y2'].value()) or int(bounding_box_form['y2'].value()) > height):
                        messages.info(request,
                                      "Valor de Y2 negativo ou superior ao tamanho da imagem, valor máximo:" + str(
                                          height))
                    else:
                        bounding_box_form.save()
                        return redirect('camera_atual',email, nome, ip)

            for box in bounding_boxes:
                action_remover_bounding_box = request.POST.get('removerBoundingBox' + str(box.id))
                action_editar_bounding_box = request.POST.get('editarBoundingBox' + str(box.id))
                if action_remover_bounding_box == 'Remover Box':
                    box.delete()
                    return redirect('camera_atual', email, nome, ip)

                if action_editar_bounding_box == "Confirmar Edição":
                    '''box.x1 = bounding_box_form['x1'].value()
                    box.save()'''

                    if bounding_box_form.is_valid():
                        box.delete()
                        bounding_box_form.save()
                    return redirect('camera_atual', email, nome, ip)

            partitions = {}
            cwd = os.getcwd()
            for i in range(len(bounding_boxes)):
                dict = bounding_boxes[i].to_dict()
                partitions[str(bounding_boxes[i].id)] = dict
            with open(os.path.join(cwd, 'jsons', 'camera{}.json'.format(ip)), "w") as out_file:
                json.dump(partitions, out_file, indent=2)

    return render(request, "camera_view.html", context)


def camera_edit_view(request, email, nome, ip):
    action_cancelar = request.GET.get('cancelar')
    if action_cancelar == "Cancelar":
        return redirect("ambientes", email)

    context = {}
    context['data'] = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.get(cliente_id=context['data'].id, nome=nome)
    cameras = Camera.objects.all()
    camera = cameras.filter(ambiente_id=ambiente.id, ip=ip)
    context['ambiente_name'] = nome
    camera = camera[0]
    context['camera'] = camera

    form = CameraForm(request.POST or None, initial={'ip':camera.ip,
                                                     'usuario':camera.usuario,
                                                     'senha': camera.senha,
                                                     'porta':camera.porta,
                                                     'ambiente_id':camera.ambiente_id,
                                                     'num_boundingbox':camera.num_boundingbox})


    flag_cam_existente = False
    if (camera != None) and (camera != []):
        for cam in cameras:
            if cam.get_nome() == form['nome'].value():
                flag_cam_existente = True
                break



    try:
        if form.is_valid() and not flag_cam_existente:
            camera.delete()
            form.save()
            return redirect('ambientes', email)
        elif (form.is_valid() and flag_cam_existente):
            raise ValidationError('errou')

    except ValidationError:
        messages.info(request, 'Câmera com esse nome já existe ou o nome não está sendo modificado!')

    context['form'] = form
    context['nome_in_edit'] = nome
    return render(request, "camera_edit_view.html", context)

def camera_create_view(request, email, nome):
    context = {}
    context['data'] = Cliente.objects.get(email=email)
    context['ambiente'] = Ambiente.objects.get(cliente_id=context['data'].id, nome=nome)
    cameras = Camera.objects.all()
    form = CameraForm(request.POST or None, initial={"ambiente_id": context['ambiente'].id})
    flag_cam_existe = False
    if (cameras != None) and (cameras != []):
        for cam in cameras:
            if cam.get_ip() == form['ip'].value():
                flag_cam_existe = True
                break
    try:
        if form.is_valid() and not flag_cam_existe:
            form.save()
            return redirect('ambiente_atual',email, nome)
        elif(form.is_valid() and flag_cam_existe):
            raise ValidationError('errou')

    except ValidationError:
        messages.info(request, 'A câmera com o ip informado já existe')
    
    context['form'] = form
    return render(request, "camera_create_view.html", context)

def remover_bounding_box(bounding_box_id):
    bounding_box = BoundingBox.objects.get(id=bounding_box_id)[0]

    if bounding_box != None:
        bounding_box.delete()

def remover_camera(email, nome, cam_ip):
    cliente = Cliente.objects.get(email=email)
    ambientes = Ambiente.objects.all()
    ambiente = ambientes.get(cliente_id=cliente.id, nome=nome)
    cameras = Camera.objects.all()
    camera = cameras.filter(ambiente_id=ambiente.id, ip=cam_ip)

    if camera != None and len(camera) > 0:
        camera.delete()

class VideoCamera(object):
    def __init__(self, usuario, senha, ip, porta):
        self.video = cv2.VideoCapture("rtsp://{}:{}@{}:{}".format(usuario, senha, ip, porta))

    def __del__(self):
        self.video.release()

    def get_frame(self, ip):
        ret, frame = self.video.read()
        frame_width = int(frame.shape[0]*0.7)
        frame_height = int(frame.shape[1]*0.7)
        frame = cv2.resize(frame,(frame_height,frame_width),interpolation=cv2.INTER_AREA)
        bounding_box = BoundingBox.objects.all().filter(camera_ip = ip)
        frame_box = frame
        for i in bounding_box:
            frame_box = cv2.rectangle(frame_box, (i.x1,i.y1),(i.x2,i.y2),  tuple(int(str(i.cor)[j:j+2], 16) for j in (0, 2, 4)),2)
        ret, frame_box = cv2.imencode('.jpg', frame_box)
        set_shape(frame_width, frame_height)
        return frame_box.tobytes()

def gen(camera, ip):
    while True:
        frame = camera.get_frame(ip)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request, usuario, senha, ip, porta):
    return StreamingHttpResponse(gen(VideoCamera(usuario, senha, ip, porta),ip),
                    content_type='multipart/x-mixed-replace; boundary=frame')

def set_shape(imagem_width, imagem_height):
    global width
    width = imagem_width
    global height
    height = imagem_height