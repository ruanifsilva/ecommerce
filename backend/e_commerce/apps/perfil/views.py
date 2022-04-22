import copy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from django.contrib import messages

from apps.perfil.forms import PerfilForm, UserForm
from apps.perfil.models import Perfil


class BasePerfil(View):
    template_name = "perfil/criar.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get("carrinho", {}))
        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = Perfil.objects.filter(usuario=self.request.user).first()

            self.contexto = {
                "userform": UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                "perfilform": PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil,
                ),
            }
        else:
            self.contexto = {
                "userform": UserForm(data=self.request.POST or None),
                "perfilform": PerfilForm(data=self.request.POST or None),
            }

        self.userform = self.contexto["userform"]
        self.perfilform = self.contexto["perfilform"]

        if self.request.user.is_authenticated:
            self.template_name = "perfil/atualizar.html"
        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class CriarPerfil(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                "Existem erros em seu formulário, por favor verifique e tente novamente",
            )
            return self.renderizar

        username = self.userform.cleaned_data.get("username")
        password = self.userform.cleaned_data.get("password")
        email = self.userform.cleaned_data.get("email")
        first_name = self.userform.cleaned_data.get("first_name")
        last_name = self.userform.cleaned_data.get("last_name")

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.perfilform.cleaned_data["usuario"] = usuario
                print(self.perfilform.cleaned_data)
                perfil = Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
        # Usuário não logado(novo)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(self.request, username=usuario, password=password)

            if autentica:
                login(self.request, user=usuario)

        self.request.session["carrinho"] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request, "Seu cadastro foi criado ou atualizado com sucesso"
        )

        messages.success(
            self.request, "Login feito com sucesso, pode fazer suas compras."
        )

        return redirect("produto:carrinho")
        return self.renderizar


class AtualizarPerfil(View):
    pass


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")

        if not username or not password:
            messages.error(self.request, "Usuário ou senha inválidos")
            return redirect("perfil:criar")

        usuario = authenticate(self.request, username=username, password=password)

        if not usuario:
            messages.error(self.request, "Usuário ou senha inválidos")
            return redirect("perfil:criar")

        messages.success(self.request, "Login realizado com sucesso")
        login(self.request, user=usuario)
        return redirect("produto:carrinho")


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get("carrinho"))
        logout(self.request)
        self.request.session["carrinho"] = carrinho
        self.request.session.save()
        return redirect("produto:lista")
