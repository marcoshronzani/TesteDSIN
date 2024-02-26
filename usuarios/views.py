from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth


def cadastro(request):
    if request.user.is_authenticated:
        return redirect(reverse("agendamentos"))

    if request.method == "GET":
        return render(request, "cadastro.html")

    elif request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if (
            len(nome.strip()) == 0
            or len(email.strip()) == 0
            or len(senha.strip()) == 0
            or len(confirmar_senha.strip()) == 0
        ):
            messages.add_message(request, constants.ERROR, "Preencher todos os campos")
            return redirect(reverse("cadastro"))

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "Senhas não coincidem.")
            return redirect(reverse("cadastro"))

        usuario = User.objects.filter(username=email)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, "Usuário já cadastrado")
            return redirect(reverse("cadastro"))

        usuario = User.objects.create_user(
            username=email, first_name=nome, email=email, password=senha
        )
        return redirect(reverse("login"))


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("agendamentos"))

    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        usuario = auth.authenticate(username=email, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, "Usuário ou Senha inválidos")
            return redirect(reverse("login"))

        auth.login(request, usuario)
        return redirect(reverse("home"))


def sair(request):
    auth.logout(request)
    return redirect(reverse("login"))
