# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alunos.views import AlunoViewSet
from cursos.views import CursoViewSet
from matriculas.views import MatriculaViewSet
from financeiro.views import TransacaoViewSet, RelatorioView
from core.views import dashboard_geral, historico_aluno

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'matriculas', MatriculaViewSet)
router.register(r'transacoes', TransacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/relatorios/', RelatorioView.as_view(), name='relatorios'),
    path('dashboard/', dashboard_geral, name='dashboard'),
    path('aluno/<int:aluno_id>/historico/', historico_aluno, name='historico_aluno'),
]