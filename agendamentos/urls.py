from django.urls import path
from . import views

urlpatterns = [
    path("servicos/", views.servicos, name="servicos"),
    path("novo_servico", views.novo_servico, name="novo_servico"),
    path("editar_servico/<int:id>", views.editar_servico, name="editar_servico"),
    path("excluir_servico/<int:id>", views.excluir_servicos, name="excluir_servico"),
    path("agendamentos/", views.agendamentos, name="agendamentos"),
    path("novo_agendamento/", views.novo_agendamento, name="novo_agendamento"),
    path(
        "editar_agendamento/<int:id>",
        views.editar_agendamento,
        name="editar_agendamento",
    ),
    path(
        "excluir_agendamento/<int:id>",
        views.excluir_agendamento,
        name="excluir_agendamento",
    ),
    path(
        "aprovacao_agendamentos",
        views.aprovacao_agendamentos,
        name="aprovacao_agendamentos",
    ),
    path(
        "acompanhamento_negocio/",
        views.acompanhamento_negocio,
        name="acompanhamento_negocio",
    ),
]
