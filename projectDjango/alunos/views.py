from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Aluno
from .serializers import AlunoSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        aluno = self.get_object()
        data = {
            'aluno': AlunoSerializer(aluno).data,
            'matriculas': aluno.matriculas.count(),
            'total_pago': aluno.total_pago,
            'total_devido': aluno.total_devido,
            'matriculas_pagas': aluno.matriculas.filter(status_pagamento='pago').count(),
            'matriculas_pendentes': aluno.matriculas.filter(status_pagamento='pendente').count(),
        }
        return Response(data)