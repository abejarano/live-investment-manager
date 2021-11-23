from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

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

    def save_model(self, request, obj, form, change):
        obj.user = User.objects.get(username=request.user)
        obj.save()
