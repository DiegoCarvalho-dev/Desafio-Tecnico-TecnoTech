from django.contrib import admin
from django.urls import path
from alunos.views import historico_aluno
from financeiro.views import dashboard_geral

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_geral, name='dashboard'),
    path('aluno/<int:aluno_id>/historico/', historico_aluno, name='historico_aluno'),
]