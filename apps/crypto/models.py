from django.db import models


# Create your models here.

class Crypto(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False, verbose_name='Activo financiero')
    price = models.DecimalField(max_digits=19, decimal_places=8, verbose_name='Precio de mercado')
    status = models.BooleanField(default=True, verbose_name='Activo?')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_crypto'
        verbose_name = 'Criptomoneda'
        verbose_name_plural = 'Criptomonedas'
