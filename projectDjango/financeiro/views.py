from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Transacao
from .serializers import TransacaoSerializer
from alunos.models import Aluno
from cursos.models import Curso
from matriculas.models import Matricula


class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RelatorioView(generics.GenericAPIView):
    def get(self, request):
        total_alunos = Aluno.objects.count()
        cursos_ativos = Curso.objects.filter(status='ativo').count()

        matriculas = Matricula.objects.all()
        matriculas_pagas = matriculas.filter(status_pagamento='pago').count()
        matriculas_pendentes = matriculas.filter(status_pagamento='pendente').count()

        total_recebido = sum(
            matricula.total_pagamentos
            for matricula in matriculas.filter(status_pagamento='pago')
        )

        total_pendente = sum(
            matricula.saldo_devido
            for matricula in matriculas.filter(status_pagamento='pendente')
        )

        matriculas_por_curso = []
        for curso in Curso.objects.all():
            matriculas_por_curso.append({
                'curso': curso.nome,
                'total_matriculas': curso.matriculas.count(),
                'matriculas_pagas': curso.matriculas.filter(status_pagamento='pago').count(),
                'matriculas_pendentes': curso.matriculas.filter(status_pagamento='pendente').count(),
                'valor_total_gerado': sum(m.curso.valor_inscricao for m in curso.matriculas.all())
            })

        return Response({
            'dashboard': {
                'total_alunos': total_alunos,
                'cursos_ativos': cursos_ativos,
                'matriculas_pagas': matriculas_pagas,
                'matriculas_pendentes': matriculas_pendentes,
                'total_recebido': total_recebido,
                'total_pendente': total_pendente,
            },
            'matriculas_por_curso': matriculas_por_curso,
            'top_alunos': [
                {
                    'aluno': aluno.nome,
                    'total_pago': aluno.total_pago,
                    'total_matriculas': aluno.matriculas.count()
                }
                for aluno in Aluno.objects.all()[:5]  # Top 5 alunos
            ]
        })