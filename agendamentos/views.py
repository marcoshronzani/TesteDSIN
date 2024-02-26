from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Servico, Agendamento
from django.db.models.functions import ExtractWeek
from django.db.models import Sum


@login_required
def servicos(request):
    if request.user.is_superuser:
        if request.method == "GET":
            servicos = Servico.objects.all()

            return render(request, "servicos.html", {"servicos": servicos})

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )

    return redirect(reverse("home"))


@login_required
def novo_servico(request):
    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, "novo_servico.html")

        elif request.method == "POST":
            descricao = request.POST.get("descricao")
            valor = request.POST.get("valor").replace(",", ".")

            if len(descricao.strip()) == 0 or len(valor.strip()) == 0:
                messages.add_message(
                    request, constants.ERROR, "Preencher todos os campos"
                )
                return redirect(reverse("novo_servico"))

            try:
                servico = Servico(descricao=descricao, valor=valor)
                servico.save()
                messages.add_message(request, constants.SUCCESS, "Serviço Cadastrado")
                return redirect(reverse("servicos"))

            except:
                messages.add_message(
                    request, constants.ERROR, "Erro ao criar o serviço"
                )
                return redirect(reverse("novo_servico"))

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )

    return redirect(reverse("home"))


@login_required
def editar_servico(request, id):
    if request.user.is_superuser:
        servico = Servico.objects.get(id=id)
        if request.method == "GET":

            return render(request, "editar_servico.html", {"servico": servico})

        elif request.method == "POST":
            descricao = request.POST.get("descricao")
            valor = request.POST.get("valor").replace(",", ".")

            if len(descricao.strip()) == 0 or len(valor.strip()) == 0:
                messages.add_message(
                    request, constants.ERROR, "Preencher todos os campos"
                )
                return redirect(f"/agendamentos/editar_servico/{id}")

            try:
                servico.descricao = descricao
                servico.valor = valor
                servico.save()
                messages.add_message(request, constants.SUCCESS, "Edição realizada!")
            except:
                messages.add_message(request, constants.ERROR, "Erro ao editar Produto")
                return redirect(f"/agendamentos/editar_servico/{id}")

            return redirect(reverse("servicos"))

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )

    return redirect(reverse("home"))


@login_required
def excluir_servicos(request, id):
    if request.user.is_superuser:
        Servico.objects.get(id=id).delete()
        messages.add_message(request, constants.SUCCESS, "Exclusão Realizada")
        return redirect(reverse("servicos"))

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )

    return redirect(reverse("home"))


@login_required
def agendamentos(request):
    if request.method == "GET":
        usuario = User.objects.get(id=request.user.id)
        data_inicio = request.GET.get("data_inicio")
        data_fim = request.GET.get("data_fim")

        agendamentos = Agendamento.objects.filter(usuario=usuario).order_by(
            "-data_agendamento"
        )

        if usuario.is_superuser:
            agendamentos = Agendamento.objects.all().order_by("-data_agendamento")

        if data_inicio and data_fim:
            try:
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                data_fim = (
                    datetime.strptime(data_fim, "%Y-%m-%d")
                    + timedelta(days=1)
                    - timedelta(seconds=1)
                )
                agendamentos = agendamentos.filter(
                    data_agendamento__range=[data_inicio, data_fim]
                ).order_by("-data_agendamento")
            except ValueError:
                messages.add_message(
                    request, constants.ERROR, "Preencha as datas corretamente"
                )
                return redirect(reverse("agendamentos"))

        return render(request, "agendamentos.html", {"agendamentos": agendamentos})


@login_required
def novo_agendamento(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        return render(request, "novo_agendamento.html", {"servicos": servicos})

    elif request.method == "POST":
        data = request.POST.get("data")
        servicos = request.POST.getlist("servicos")

        if len(data.strip()) == 0 or not servicos:
            messages.add_message(
                request, constants.ERROR, "Favor Preencher todos os campos"
            )
            return redirect(reverse("novo_agendamento"))

        data_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M")
        semana = data_obj.strftime(
            "%W"
        )  # Obter a semana do ano considerando segunda-feira como o primeiro dia da semana

        agendamento_na_semana = (
            Agendamento.objects.annotate(semana_do_ano=ExtractWeek("data_agendamento"))
            .filter(semana_do_ano=semana, usuario=request.user)
            .first()
        )

        if (
            agendamento_na_semana
            and agendamento_na_semana.data_agendamento.day != data_obj.day
        ):
            messages.add_message(
                request,
                constants.ERROR,
                f"Você já possui agendamendo na data {agendamento_na_semana.data_agendamento}, faça o novo agendamento para mesma data",
            )
            return redirect(reverse("novo_agendamento"))

        try:
            agendamento = Agendamento(data_agendamento=data, usuario=request.user)
            agendamento.save()

            for servico_id in servicos:
                servico = Servico.objects.get(id=servico_id)
                agendamento.servico.add(servico)

            agendamento.save()
            messages.add_message(request, constants.SUCCESS, "Agendamento Cadastrado")

            return redirect(reverse("agendamentos"))

        except:
            messages.add_message(
                request, constants.ERROR, "Erro ao Adicionar Agendamento"
            )
            return redirect(reverse("novo_agendamento"))


@login_required
def editar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    if request.method == "GET":
        servicos = Servico.objects.all()

        data_limite = agendamento.data_agendamento - timedelta(days=2)

        if datetime.now() > data_limite and not request.user.is_superuser:
            messages.add_message(
                request,
                constants.ERROR,
                "Não é possivel alterar o agendamento com menos de 2 dias de antecedencia, entrar em contato por telefone",
            )
            return redirect(reverse("agendamentos"))

        context = {
            "agendamento": agendamento,
            "servicos": servicos,
            "data_formatada": agendamento.data_agendamento.strftime("%Y-%m-%dT%H:%M"),
        }

        return render(request, "editar_agendamento.html", context)

    elif request.method == "POST":
        data = request.POST.get("data")
        servicos = request.POST.getlist("servicos")

        if len(data.strip()) == 0 or not servicos:
            messages.add_message(
                request, constants.ERROR, "Favor Preencher todos os campos"
            )
            return redirect(f"/agendamentos/editar_agendamento/{id}")

        if not request.user.is_superuser:
            data_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M")
            semana = data_obj.strftime(
                "%W"
            )  # Obter a semana do ano considerando segunda-feira como o primeiro dia da semana

            agendamento_na_semana = (
                Agendamento.objects.annotate(
                    semana_do_ano=ExtractWeek("data_agendamento")
                )
                .filter(semana_do_ano=semana, usuario=request.user)
                .first()
            )

            if (
                agendamento_na_semana
                and agendamento_na_semana.data_agendamento.day != data_obj.day
            ):
                messages.add_message(
                    request,
                    constants.ERROR,
                    f"Você já possui agendamendo na data {agendamento_na_semana.data_agendamento}, faça o novo agendamento para mesma data",
                )
                return redirect(f"/agendamentos/editar_agendamento/{id}")

        agendamento.data_agendamento = data
        agendamento.servico.clear()
        for servico_id in servicos:
            servico = Servico.objects.get(id=servico_id)
            agendamento.servico.add(servico)

        agendamento.save()

        return redirect(reverse("agendamentos"))


@login_required
def excluir_agendamento(request, id):
    if request.user.is_superuser:
        Agendamento.objects.get(id=id).delete()
        messages.add_message(request, constants.SUCCESS, "Exclusão Realizada")
        return redirect(reverse("agendamentos"))

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )

    return redirect(reverse("home"))


@login_required
def aprovacao_agendamentos(request):
    if request.user.is_superuser:
        if request.method == "GET":
            usuario = User.objects.get(id=request.user.id)

            agendamentos = Agendamento.objects.filter(usuario=request.user.id).order_by(
                "-data_agendamento"
            )
            if usuario.is_superuser:
                agendamentos = Agendamento.objects.all().order_by("-data_agendamento")

            return render(
                request, "aprovacao_agendamentos.html", {"agendamentos": agendamentos}
            )

        elif request.method == "POST":
            status = request.POST.get("status")
            id_agendamento = request.POST.get("id_agendamento")

            agendamento = Agendamento.objects.get(id=id_agendamento)
            agendamento.status = status
            agendamento.save()
            messages.add_message(
                request,
                constants.SUCCESS,
                f"O agendamento de {agendamento.usuario.first_name}, foi alterado.",
            )

            return redirect(reverse("aprovacao_agendamentos"))

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )

    return redirect(reverse("home"))


@login_required
def acompanhamento_negocio(request):
    if request.user.is_superuser:
        if request.method == "GET":
            data_inicio = request.GET.get("data_inicio")
            data_fim = request.GET.get("data_fim")

            agendamentos = Agendamento.objects.all()

            if data_inicio and data_fim:
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                data_fim = (
                    datetime.strptime(data_fim, "%Y-%m-%d")
                    + timedelta(days=1)
                    - timedelta(seconds=1)
                )
                agendamentos = agendamentos.filter(
                    data_agendamento__range=[data_inicio, data_fim], status="FN"
                )
                quantidade_agendamentos = agendamentos.count()
                soma_valores = agendamentos.aggregate(soma=Sum("servico__valor"))[
                    "soma"
                ]

                context = {
                    "quantidade": quantidade_agendamentos,
                    "soma_valores": soma_valores,
                }

                return render(request, "acompanhamento_negocio.html", context)
            agendamentos = agendamentos.filter(status="FN")
            agendamentos_total = agendamentos.count()
            valor_total = agendamentos.aggregate(soma=Sum("servico__valor"))["soma"]

            context = {
                "quantidade_total": agendamentos_total,
                "valor_total": valor_total,
            }

            return render(request, "acompanhamento_negocio.html", context)

    messages.add_message(
        request, constants.ERROR, "Permitido apenas para administradores"
    )
    return redirect(reverse("home"))
