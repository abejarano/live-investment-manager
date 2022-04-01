from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

from apps.crypto.models import Crypto


class Capital(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    capital = models.DecimalField(max_digits=19, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_capital'
        verbose_name = 'Capital'
        verbose_name_plural = 'Capitales'


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

    def ROI(self):
        current_balance = self.amount_crypto * self.crypto.price
        roi = round(current_balance - self.amount, 2)

        if roi < 0:
            return mark_safe('<b style = "color: red">' + str(roi) + '</b>')

        return mark_safe('<b style = "color: green">' + str(roi) + '</b>')

    def precio_actual(self):
        return str(self.crypto.price)

    def delete(self, *args, **kwargs):
        super(Investment, self).delete(*args, **kwargs)
        capital = Capital.objects.all().first()
        capital.capital = capital.capital - self.amount
        capital.update()

    class Meta:
        db_table = 'tb_investments'
        verbose_name = 'Inversiones'
        verbose_name_plural = 'Inversiones'
