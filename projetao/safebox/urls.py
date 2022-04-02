from django.urls import path

from . import views

app_name = "safebox"

urlpatterns=[
    path("",views.cliente_create_view, name="cadastrar"),
    path("<email>/",views.cliente_detail_view, name="visualizar"),
    path("<email>/editar",views.cliente_edit_view, name="editar")
]