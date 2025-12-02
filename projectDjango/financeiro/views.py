from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alunos.models import Aluno
from cursos.models import Curso
from matriculas.models import Matricula


@login_required
def dashboard_geral(request):
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

    context = {
        'total_alunos': total_alunos,
        'cursos_ativos': cursos_ativos,
        'matriculas_pagas': matriculas_pagas,
        'matriculas_pendentes': matriculas_pendentes,
        'total_recebido': total_recebido,
        'total_pendente': total_pendente,
    }

    return render(request, 'financeiro/dashboard.html', context)