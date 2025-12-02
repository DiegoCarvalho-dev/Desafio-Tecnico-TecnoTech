# core/views.py
from django.shortcuts import render, get_object_or_404
from alunos.models import Aluno
from cursos.models import Curso
from matriculas.models import Matricula
from financeiro.models import Transacao
from django.db.models import Sum


def dashboard_geral(request):
    total_alunos = Aluno.objects.count()
    cursos_ativos = Curso.objects.filter(status='ativo').count()

    matriculas_pagas = Matricula.objects.filter(status_pagamento='pago').count()
    matriculas_pendentes = Matricula.objects.filter(status_pagamento='pendente').count()

    total_recebido = Transacao.objects.filter(matricula__status_pagamento='pago').aggregate(
        total=Sum('valor')
    )['total'] or 0

    total_pendente = Matricula.objects.filter(status_pagamento='pendente').aggregate(
        total=Sum('curso__valor_inscricao')
    )['total'] or 0

    context = {
        'total_alunos': total_alunos,
        'cursos_ativos': cursos_ativos,
        'matriculas_pagas': matriculas_pagas,
        'matriculas_pendentes': matriculas_pendentes,
        'total_recebido': total_recebido,
        'total_pendente': total_pendente,
    }
    return render(request, 'financeiro/dashboard.html', context)


def historico_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    matriculas = Matricula.objects.filter(aluno=aluno).select_related('curso')

    total_pago = Transacao.objects.filter(matricula__aluno=aluno).aggregate(
        total=Sum('valor')
    )['total'] or 0

    total_devido = Matricula.objects.filter(aluno=aluno, status_pagamento='pendente').aggregate(
        total=Sum('curso__valor_inscricao')
    )['total'] or 0

    matriculas_com_info = []
    for matricula in matriculas:
        total_pagamentos = Transacao.objects.filter(matricula=matricula).aggregate(
            total=Sum('valor')
        )['total'] or 0
        saldo_devido = matricula.curso.valor_inscricao - total_pagamentos

        matriculas_com_info.append({
            'curso': matricula.curso,
            'data_matricula': matricula.data_matricula,
            'status_pagamento': matricula.status_pagamento,
            'get_status_pagamento_display': matricula.get_status_pagamento_display(),
            'valor_inscricao': matricula.curso.valor_inscricao,
            'total_pagamentos': total_pagamentos,
            'saldo_devido': saldo_devido,
        })

    context = {
        'aluno': {
            'nome': aluno.nome,
            'email': aluno.email,
            'total_pago': total_pago,
            'total_devido': total_devido,
        },
        'matriculas': matriculas_com_info,  # Agora é lista de dicionários
    }
    return render(request, 'alunos/historico.html', context)

