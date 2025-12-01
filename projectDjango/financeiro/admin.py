from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'tipo', 'valor', 'data', 'descricao')
    list_filter = ('tipo', 'data', 'matricula__aluno')
    search_fields = ('matricula__aluno__nome', 'matricula__curso__nome', 'descricao')
    autocomplete_fields = ['matricula']
    list_per_page = 20
    date_hierarchy = 'data'