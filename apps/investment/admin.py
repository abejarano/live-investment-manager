from decimal import Decimal

from admincharts.admin import AdminChartMixin
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from apps.investment.forms import FormInvestment
from apps.investment.models import Investment, Capital


@admin.register(Investment)
class AdminInvestment(AdminChartMixin, admin.ModelAdmin):
    roi = 0
    list_display = ['crypto', 'price_crypto', 'precio_actual', 'amount', 'amount_crypto', 'ROI']
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
        # extra_context = extra_context or {}
        # capital = Capital.objects.get(user=request.user.id)
        # extra_context['capital'] = capital.capital
        #
        # print(self.RIO )
        #
        # return super(AdminInvestment, self).changelist_view(request, extra_context)

        capital = Capital.objects.get(user=request.user.id)

        response = super().changelist_view(request, extra_context)
        response.context_data['ROI'] = round(self.roi, 2)

        response.context_data['capital'] = round(capital.capital, 2)
        response.context_data['capital_actual'] = round(capital.capital + self.roi, 2)

        return response

    def save_model(self, request, obj, form, change):
        obj.user = User.objects.get(username=request.user)

        if not change:
            try:
                capital = Capital.objects.get(user__username=request.user)
                capital.capital = capital.capital + obj.amount
                capital.save()

            except ObjectDoesNotExist:
                Capital(
                    user=obj.user,
                    capital=obj.amount
                ).save()

        obj.save()

    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        labels = []
        totals = []
        aux = {}
        self.roi = 0
        for crypto_query in queryset:
            amount = crypto_query.amount
            if crypto_query.crypto.name in aux.keys():
                amount = Decimal(aux[crypto_query.crypto.name]) + amount

            current_balance = crypto_query.amount_crypto * crypto_query.crypto.price
            self.roi = self.roi + (current_balance - crypto_query.amount)

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
