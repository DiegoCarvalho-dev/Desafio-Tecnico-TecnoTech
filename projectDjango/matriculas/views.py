from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Matricula
from .serializers import MatriculaSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def marcar_como_pago(self, request, pk=None):
        matricula = self.get_object()

        from financeiro.models import Transacao
        Transacao.objects.create(
            matricula=matricula,
            valor=matricula.saldo_devido,
            tipo='pagamento',
            descricao='Pagamento via API'
        )

        matricula.atualizar_status_pagamento()

        return Response({
            'message': f'Matrícula {matricula.id} marcada como paga',
            'transacao_criada': True,
            'novo_status': matricula.status_pagamento
        })