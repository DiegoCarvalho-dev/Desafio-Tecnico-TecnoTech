from django.db import models
from alunos.models import Aluno
from cursos.models import Curso

class Matricula(models.Model):
    STATUS_CHOICES = (
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
    )

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='matriculas')

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')

    data_matricula = models.DateField(auto_now_add=True)

    status_pagamento = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'{self.aluno.nome} - {self.curso.nome} ({self.get_status_pagamento_display()})'

    class Meta:
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'

        unique_together = ('aluno', 'curso')
        ordering = ['-data_matricula']
