from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from apps.produto import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = "produto/lista.html"
    context_object_name = "produtos"
    paginate_by = 1


class DetalheProduto(View):
    pass


class AdicionarAoCarrinho(View):
    pass


class RemoverDoCarrinho(View):
    pass


class Carrinho(View):
    pass


class FinalizarCompra(View):
    pass
