from django.contrib import admin
from .models import Matricula

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula', 'status_pagamento', 'valor_pago')
    list_filter = ('status_pagamento', 'data_matricula', 'curso')
    search_fields = ('aluno__nome', 'curso__nome')
    autocomplete_fields = ['aluno', 'curso']
    list_per_page = 20