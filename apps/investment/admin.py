from django.contrib import admin

# Register your models here.
from apps.investment.models import Investment


@admin.register(Investment)
class AdminInvestment(admin.ModelAdmin):
    list_display = ['crypto', 'price_crypto', 'amount', 'amount_crypto']
    add_form_template = 'investment/form_add_investment.html'
    fieldsets = [
        (None, {
            'fields': [
                ('crypto',),
                ('price_crypto', 'amount', 'amount_crypto',)
            ]
        }

         )
    ]
