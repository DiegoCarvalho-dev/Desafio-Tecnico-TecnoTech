from django.contrib import admin

from alunos.models import Aluno
from .models import Curso


@admin.register(Curso)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carga_horaria', 'valor_inscricao', 'status', 'data_criacao')

    list_filter = ('status',)
    search_fields = ('nome',)
    list_per_page = 20
    ordering = ('nome',)