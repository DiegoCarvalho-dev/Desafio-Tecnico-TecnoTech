from django.db import models


class Curso(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )

    nome = models.CharField(max_length=200)

    carga_horaria = models.IntegerField(help_text='Carga horária em horas')

    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'