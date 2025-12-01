from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Aluno


@login_required
def historico_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    context = {
        'aluno': aluno,
        'matriculas': aluno.matriculas.all(),
        'total_pago': aluno.total_pago,
        'total_devido': aluno.total_devido,
        'transacoes': aluno.historico_transacoes,
    }

    return render(request, 'alunos/historico.html', context)