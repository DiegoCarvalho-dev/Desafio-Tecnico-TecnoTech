from rest_framework import serializers
from .models import Aluno


class AlunoSerializer(serializers.ModelSerializer):
    total_pago = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_devido = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Aluno
        fields = '__all__'
        read_only_fields = ('data_criacao',)