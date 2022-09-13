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
    amount = models.DecimalField(max_digits=19, decimal_places=8, verbose_name='Monto invertido (USD)')
    amount_crypto = models.DecimalField(max_digits=19, decimal_places=8, verbose_name='Cantidad de cripto')
    price_crypto = models.DecimalField(
        max_digits=19,
        decimal_places=8,
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

    def GRAFICO(self):
        return mark_safe(
            '<a target="_blank" href="https://www.binance.com/en/trade/' + self.crypto.name + '_USDT?theme=dark&type=spot">'
                                                                                              '<img src="https://bin.bnbstatic.com/static/images/common/favicon.ico" />'
                                                                                              '</a>'
        )

    def delete(self, *args, **kwargs):
        super(Investment, self).delete(*args, **kwargs)
        capital = Capital.objects.all().first()
        capital.capital = capital.capital - self.amount
        capital.update()

    class Meta:
        db_table = 'tb_investments'
        verbose_name = 'Inversiones'
        verbose_name_plural = 'Inversiones'


class InvestmentReturnProjection(models.Model):
    investment = models.OneToOneField(
        Investment,
        related_name='return_projection',
        on_delete=models.CASCADE
    )
    estimated_price = models.DecimalField(
        max_digits=19,
        decimal_places=8,
        help_text='Precio que se espera que la inversión alcance a la fecha estiamda.',
        verbose_name='Precio estimado'
    )
    execution_date = models.DateField(
        null=False, blank=False,
        verbose_name='Fecha estimada'
    )

    rio = models.DecimalField(
        max_digits=19,
        decimal_places=8,
        verbose_name='ROI'
    )

    def crypto(self):
        return self.investment.crypto

    def Monto_invertido(self):
        return str(self.investment.amount)

    class Meta:
        db_table = 'tb_projection'
        verbose_name = 'Proyección'
        verbose_name_plural = 'Proyecciones'
