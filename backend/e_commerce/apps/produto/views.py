from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.produto import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = "produto/lista.html"
    context_object_name = "produtos"
    paginate_by = 5


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = "produto/detalhe.html"
    context_object_name = "produto"
    slug_url_kwarg = "slug"


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get("HTTP_REFERER", reverse("produto:lista"))

        variacao_id = self.request.GET.get("vid")

        if not variacao_id:
            messages.error(self.request, "Produto não existe")
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        if not self.request.session.get("carrinho"):
            self.request.session["carrinho"] = {}
            self.request.session.save()

        carrinho = self.request.session["carrinho"]

        if variacao_id in carrinho:
            # TODO: Variação existe no carrinho
            pass
        else:
            # TODO:Variação não existe no carrinho
            pass

        return HttpResponse("Adicionar ao carrinho")


class RemoverDoCarrinho(View):
    pass


class Carrinho(View):
    pass


class FinalizarCompra(View):
    pass
