from django.urls import path, include

from . import views

app_name = "safebox"

urlpatterns=[
    path("cadastrar/", views.cliente_create_view, name="cadastrar"),
    path("", views.cliente_login_view, name="login"),
    path("home/<email>/", views.home_view, name="home"),
    path("visualizar/<email>/", views.cliente_detail_view, name="visualizar"),
    path("editar/<email>/", views.cliente_edit_view, name="editar"),
    path("assinar/plano/<email>/",views.assinatura_create_view, name="assinar_plano"),
    path("visualizar/plano/<email>", views.cliente_assinatura_view, name="visualizar_assinatura"),
    path('plano/trocar/<email>', views.assinatura_trocar_view, name='trocar_assinatura'),
    path("ambientes/<email>/", views.ambiente_list_view, name="ambientes"),
    path("ambientes/<email>/cadastar", views.ambiente_create_view, name="criar_ambiente"),
    path('ambientes/<email>/visualizar/<nome>', views.ambiente_view, name='ambiente_atual'),
    path("ambientes/<email>/editar/<nome>", views.ambiente_edit_view, name='editar_ambiente'),
    path("payments/<email>/<id>", views.payments, name='payments'),
    path("ambientes/<email>/<nome>/cameras/cadastrar", views.camera_create_view, name="criar_camera"),
    path("ambientes/<email>/<nome>/cameras/<ip>", views.camera_view, name="camera_atual"),
    path("ambientes/<email>/<nome>/cameras/<ip>/edit", views.camera_edit_view, name='camera_edit'),
    path("video_stream/<usuario>/<senha>/<ip>/<porta>", views.video_stream, name='video_stream')
]