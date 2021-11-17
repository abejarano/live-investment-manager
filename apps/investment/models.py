from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from apps.crypto.models import Crypto


class Investment(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=5, verbose_name='Monto invertido (USD)')
    amount_crypto = models.DecimalField(max_digits=19, decimal_places=8, verbose_name='Cantidad de cripto')
    price_crypto = models.DecimalField(
        max_digits=19,
        decimal_places=5,
        help_text='Precio al que se compro la cripto',
        verbose_name='Precio de compra'
    )
    crypto = models.ForeignKey(
        Crypto,
        related_name='fk_investment_crypto',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        User,
        related_name='fk_investment_user',
        on_delete=models.PROTECT,
        verbose_name='Inversor'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inversión')

    class Meta:
        db_table = 'tb_investments'
        verbose_name = 'Inversiones'
        verbose_name_plural = 'Inversiones'
