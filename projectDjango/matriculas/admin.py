from django.contrib import admin
from .models import Matricula


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        'aluno',
        'curso',
        'data_matricula',
        'status_pagamento',
        'total_pagamentos',
        'saldo_devido',
        'esta_quitada',
    )

    fields = (
        'aluno',
        'curso',
        'status_pagamento',
        'data_matricula',
    )

    readonly_fields = ('data_matricula',)

    list_filter = ('status_pagamento', 'data_matricula', 'curso')
    search_fields = ('aluno__nome', 'curso__nome')
    autocomplete_fields = ['aluno', 'curso']
    list_per_page = 20

    actions = ['marcar_como_pago']

    def marcar_como_pago(self, request, queryset):
        for matricula in queryset:
            from financeiro.models import Transacao
            if matricula.saldo_devido > 0:
                Transacao.objects.create(
                    matricula=matricula,
                    valor=matricula.saldo_devido,
                    tipo='pagamento',
                    descricao='Pagamento via admin'
                )
                matricula.atualizar_status_pagamento()
        self.message_user(request, f"{queryset.count()} matrículas marcadas como pagas")

    marcar_como_pago.short_description = "Marcar como pago (cria transação)"