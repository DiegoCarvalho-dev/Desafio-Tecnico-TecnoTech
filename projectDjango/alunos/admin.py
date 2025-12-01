from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'data_ingresso')  # Removi data_criacao
    list_display_links = ('nome', 'email')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('data_ingresso',)
    list_per_page = 20