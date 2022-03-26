from django.urls import path

from apps.produto import views

app_name = "produto"

urlpatterns = [
    path("", views.ListaProdutos.as_view(), name="lista"),
    path("<slug>", views.DetalheProduto.as_view(), name="Detalhe"),
    path(
        "adicionaraocarrinho/",
        views.AdicionarAoCarrinho.as_view(),
        name="adicionaraocarrinho",
    ),
    path(
        "removerdocarrinho/",
        views.RemoverDoCarrinho.as_view(),
        name="removerdocarrinho",
    ),
    path("carrinho/", views.Carrinho.as_view(), name="carrinho"),
    path("resumodacompra/", views.ResumoDaCompra.as_view(), name="resumodacompra"),
]
