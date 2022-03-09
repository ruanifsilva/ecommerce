from django.urls import path

from apps.perfil import views

app_name = "perfil"

urlpatterns = [
    path("", views.CriarPerfil.as_view(), name="criar"),
    path("atualizar/", views.AtualizarPerfil.as_view(), name="atualizar"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
