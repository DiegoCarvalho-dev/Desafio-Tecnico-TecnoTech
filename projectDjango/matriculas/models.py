from django.db import models
from templates.alunos.models import Aluno
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

    def __str__(self):
        return f'{self.aluno.nome} - {self.curso.nome} ({self.get_status_pagamento_display()})'

    @property
    def total_pagamentos(self):
        pagamentos = self.transacoes.filter(tipo='pagamento')
        return sum(t.valor for t in pagamentos) if pagamentos else 0

    @property
    def total_reembolsos(self):
        reembolsos = self.transacoes.filter(tipo='reembolso')
        return sum(t.valor for t in reembolsos) if reembolsos else 0

    @property
    def saldo_devido(self):
        return max(0, self.curso.valor_inscricao - self.total_pagamentos + self.total_reembolsos)

    @property
    def esta_quitada(self):
        return self.saldo_devido <= 0

    def atualizar_status_pagamento(self):
        if self.esta_quitada:
            self.status_pagamento = 'pago'
        else:
            self.status_pagamento = 'pendente'
        self.save()

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ('aluno', 'curso')
        ordering = ['-data_matricula']