from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from apps.investment.forms import FormInvestment
from apps.investment.models import Investment, Capital


@admin.register(Investment)
class AdminInvestment(admin.ModelAdmin):
    list_display = ['crypto', 'price_crypto', 'precio_actual', 'amount', 'amount_crypto', 'ROI']
    add_form_template = 'investment/form_add_investment.html'
    form = FormInvestment
    fieldsets = [
        (None, {
            'fields': [
                ('crypto',),
                ('price_crypto', 'amount', 'amount_crypto',)
            ]
        }

         )
    ]

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
