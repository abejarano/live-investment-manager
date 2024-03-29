from decimal import Decimal

from admincharts.admin import AdminChartMixin
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from apps.investment.forms import FormInvestment
from apps.investment.models import Investment, Capital, InvestmentReturnProjection


@admin.register(Investment)
class AdminInvestment(AdminChartMixin, admin.ModelAdmin):
    roi = 0
    capital = 0
    list_display = ['crypto', 'price_crypto', 'precio_actual', 'amount', 'amount_crypto', 'ROI', 'GRAFICO']
    add_form_template = 'investment/form_add_investment.html'
    change_list_template = 'investment/form_list_investment.html'

    form = FormInvestment
    fieldsets = [
        (None, {
            'fields': [
                ('crypto',),
                ('price_crypto', 'amount', 'amount_crypto',)
            ]
        })
    ]

    def changelist_view(self, request, extra_context=None):

        response = super().changelist_view(request, extra_context)
        response.context_data['ROI'] = round(self.roi, 2)

        response.context_data['capital'] = round(self.capital, 2)
        response.context_data['capital_actual'] = round(self.capital + self.roi, 2)

        return response

    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        labels = []
        totals = []
        aux = {}
        self.roi = 0
        self.capital = 0
        for crypto_query in queryset:
            amount = crypto_query.amount
            if crypto_query.crypto.name in aux.keys():
                amount = Decimal(aux[crypto_query.crypto.name]) + amount

            current_balance = crypto_query.amount_crypto * crypto_query.crypto.price
            self.roi = self.roi + (current_balance - crypto_query.amount)
            self.capital = self.capital + crypto_query.amount

            aux[crypto_query.crypto.name] = amount

        for crypto_name, amount in aux.items():
            labels.append(crypto_name)
            totals.append(amount)

        return {
            "labels": labels,
            "datasets": [
                {"label": "Inversión por cripto", "data": totals,
                 "backgroundColor": ["#af0cb7", "#ff8c00", "#5000ff", "#09aec8", "#15b700"]},
            ],
        }

    def save_model(self, request, obj, form, change):
        obj.user = User.objects.get(username=request.user)
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset


@admin.register(InvestmentReturnProjection)
class AdminInvestmentReturnProjection(admin.ModelAdmin):
    list_display = ['crypto', 'Monto_invertido', 'estimated_price', 'rio', 'execution_date']
