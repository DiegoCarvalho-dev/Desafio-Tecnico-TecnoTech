from django.db import models
from django.core.exceptions import ValidationError
from matriculas.models import Matricula

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('pagamento', 'Pagamento'),
        ('reembolso', 'Reembolso'),
    )

    matricula = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE,
        related_name='transacoes'
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='pagamento')
    descricao = models.TextField(blank=True)

    def clean(self):
        if self.valor > self.matricula.curso.valor_inscricao:
            raise ValidationError('Valor da transação não pode exceder o valor do curso.')
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.matricula.save()

    def __str__(self):
        return f"{self.get_tipo_display()} - R${self.valor} - {self.matricula}"

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data']

class ResumoFinanceiroAluno:
    def __init__(self, aluno):
        self.aluno = aluno

    @property
    def total_pago(self):
        total = 0
        for matricula in self.aluno.matriculas.all():
            total += matricula.total_pagamentos
        return total

    @property
    def total_devido(self):
        total = 0
        for matricula in self.aluno.matriculas.filter(status_pagamento='pendente'):
            total += matricula.saldo_devido
        return total

    @property
    def historico_transacoes(self):
        transacoes = []
        for matricula in self.aluno.matriculas.all():
            transacoes.extend(matricula.transacoes.all())
        return sorted(transacoes, key=lambda x: x.data, reverse=True)