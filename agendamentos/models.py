from django.db import models
from django.contrib.auth.models import User


class Servico(models.Model):
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descricao


class Agendamento(models.Model):
    choices_status = (
        ("AG", "Aguardando Aprovação"),
        ("AP", "Aprovado"),
        ("RC", "Recusado"),
        ("FN", "Finalizado"),
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )
    data_agendamento = models.DateTimeField()
    servico = models.ManyToManyField(Servico)
    status = models.CharField(max_length=2, choices=choices_status, default="AG")

    def __str__(self):
        return f"Agendamento: {self.data_agendamento}"
