from django.urls import path

from apps.pedido import views

app_name = "pedido"

urlpatterns = [
    path("", views.Pagar.as_view(), name="pagar"),
    path("salvarpedido/", views.SalvarPedido.as_view(), name="salvarpedido"),
    path("detalhe/", views.Detalhe.as_view(), name="detalhe"),
]
