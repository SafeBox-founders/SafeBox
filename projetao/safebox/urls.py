from django.urls import path

from . import views

app_name = "safebox"

urlpatterns=[
    path("cadastrar/", views.cliente_create_view, name="cadastrar"),
    path("", views.cliente_login_view, name="login"),
    path("home/<email>/", views.home_view, name="home"),
    path("visualizar/<email>/", views.cliente_detail_view, name="visualizar"),
    path("editar/<email>/", views.cliente_edit_view, name="editar"),
    path("assinar/plano/<email>/",views.assinatura_create_view, name="assinar_plano"),
    path("ambientes/<email>/", views.ambiente_list_view, name="ambientes"),
    path("ambientes/<email>/cadastar", views.ambiente_create_view, name="criar_ambiente"),
    path('ambientes/<email>/visualizar/<nome>', views.ambiente_view, name='ambiente_atual'),
]