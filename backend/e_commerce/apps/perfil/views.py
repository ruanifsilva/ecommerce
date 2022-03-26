from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from apps.perfil.forms import PerfilForm, UserForm
from apps.perfil.models import Perfil


class BasePerfil(View):
    template_name = "perfil/criar.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = Perfil.objects.filter(usuario=self.request.user).first()

            self.contexto = {
                "userform": UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                "perfilform": PerfilForm(data=self.request.POST or None),
            }
        else:
            self.contexto = {
                "userform": UserForm(data=self.request.POST or None),
                "perfilform": PerfilForm(data=self.request.POST or None),
            }

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class CriarPerfil(BasePerfil):
    def post(self, *args, **kwargs):

        return self.renderizar


class AtualizarPerfil(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass
