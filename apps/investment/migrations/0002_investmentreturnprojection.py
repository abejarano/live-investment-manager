# Generated by Django 4.1.1 on 2022-09-13 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentReturnProjection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_price', models.DecimalField(decimal_places=8, help_text='Precio que se espera que la inversión alcance a la fecha estiamda.', max_digits=19, verbose_name='Precio estimado')),
                ('execution_date', models.DateField(verbose_name='Fecha estimada')),
                ('rio', models.DecimalField(decimal_places=8, max_digits=19, verbose_name='ROI')),
                ('investment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='return_projection', to='investment.investment')),
            ],
            options={
                'verbose_name': 'Proyección',
                'verbose_name_plural': 'Proyecciones',
                'db_table': 'tb_projection',
            },
        ),
    ]
