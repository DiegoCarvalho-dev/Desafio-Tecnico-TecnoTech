from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_ingresso = models.DateField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    @property
    def resumo_financeiro(self):
        from templates.financeiro.models import ResumoFinanceiroAluno
        return ResumoFinanceiroAluno(self)

    @property
    def total_pago(self):
        return self.resumo_financeiro.total_pago

    @property
    def total_devido(self):
        return self.resumo_financeiro.total_devido

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'