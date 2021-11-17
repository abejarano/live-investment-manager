from django.contrib import admin

# Register your models here.
from apps.crypto.models import Crypto


@admin.register(Crypto)
class AdminCrypto(admin.ModelAdmin):
    list_display = ['name', 'price', 'status']
