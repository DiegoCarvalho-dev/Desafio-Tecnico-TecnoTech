from rest_framework import serializers
from alunos.models import Aluno
from cursos.models import Curso
from .models import Matricula
from alunos.serializers import AlunoSerializer
from cursos.serializers import CursoSerializer


class MatriculaSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)

    aluno_id = serializers.PrimaryKeyRelatedField(
        queryset=Aluno.objects.all(),
        source='aluno',
        write_only=True
    )
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(),
        source='curso',
        write_only=True
    )

    total_pagamentos = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    saldo_devido = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    esta_quitada = serializers.BooleanField(read_only=True)

    class Meta:
        model = Matricula
        fields = [
            'id', 'aluno', 'curso', 'aluno_id', 'curso_id',
            'data_matricula', 'status_pagamento',
            'total_pagamentos', 'saldo_devido', 'esta_quitada'
        ]
        read_only_fields = ('data_matricula',)