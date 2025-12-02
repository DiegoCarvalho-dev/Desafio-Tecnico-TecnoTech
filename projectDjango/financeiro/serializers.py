from rest_framework import serializers
from matriculas.models import Matricula
from .models import Transacao
from matriculas.serializers import MatriculaSerializer


class TransacaoSerializer(serializers.ModelSerializer):
    matricula = MatriculaSerializer(read_only=True)
    matricula_id = serializers.PrimaryKeyRelatedField(
        queryset=Matricula.objects.all(),
        source='matricula',
        write_only=True
    )

    class Meta:
        model = Transacao
        fields = ['id', 'matricula', 'matricula_id', 'valor', 'tipo', 'data', 'descricao']
        read_only_fields = ('data',)