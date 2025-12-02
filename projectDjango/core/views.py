# core/views.py
from django.shortcuts import render, get_object_or_404
from alunos.models import Aluno
from cursos.models import Curso
from matriculas.models import Matricula
from financeiro.models import Transacao
from django.db.models import Sum
from django.db import connection
from django.http import JsonResponse

def dashboard_geral(request):
    total_alunos = Aluno.objects.count()
    cursos_ativos = Curso.objects.filter(status='ativo').count()

    matriculas = Matricula.objects.all()
    matriculas_pagas = sum(1 for m in matriculas if m.saldo_devido <= 0)
    matriculas_pendentes = sum(1 for m in matriculas if m.saldo_devido > 0)

    total_recebido = Transacao.objects.filter(tipo='pagamento').aggregate(
        total=Sum('valor')
    )['total'] or 0

    total_pendente = sum(
        matricula.saldo_devido
        for matricula in Matricula.objects.all()
        if matricula.saldo_devido > 0
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


def historico_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    matriculas = Matricula.objects.filter(aluno=aluno).select_related('curso')

    total_pago = Transacao.objects.filter(
        matricula__aluno=aluno,
        tipo='pagamento'
    ).aggregate(total=Sum('valor'))['total'] or 0

    total_devido = sum(
        matricula.saldo_devido
        for matricula in matriculas
        if matricula.saldo_devido > 0
    )

    matriculas_com_info = []
    for matricula in matriculas:
        total_pagamentos = Transacao.objects.filter(
            matricula=matricula,
            tipo='pagamento'
        ).aggregate(total=Sum('valor'))['total'] or 0

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
        'matriculas': matriculas_com_info,
    }
    return render(request, 'alunos/historico.html', context)


def sql_bruto_relatorio(request):
    query = """
    SELECT 
        c.nome AS curso_nome,
        COUNT(m.id) AS total_matriculas,
        SUM(CASE WHEN m.status_pagamento = 'pago' THEN 1 ELSE 0 END) AS matriculas_pagas,
        SUM(CASE WHEN m.status_pagamento = 'pendente' THEN 1 ELSE 0 END) AS matriculas_pendentes,
        COALESCE(SUM(t.valor), 0) AS total_arrecadado
    FROM cursos_curso c
    LEFT JOIN matriculas_matricula m ON c.id = m.curso_id
    LEFT JOIN financeiro_transacao t ON m.id = t.matricula_id
    GROUP BY c.id, c.nome
    ORDER BY total_arrecadado DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return JsonResponse({
        'titulo': 'Relatório SQL Bruto - Total arrecadado por curso',
        'dados': results,
        'query_executada': query
    })