# Generated by Django 5.1 on 2024-12-01 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0004_alter_customuser_nr_puncte'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='locatie_livrare',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplicatie_ex.locatie'),
        ),
        migrations.AlterField(
            model_name='comanda',
            name='metoda_livrare',
            field=models.CharField(choices=[('ridicare cafenea', 'ridicare cafenea'), ('livrare la domiciliu', 'livrare la domiciliu')], max_length=50),
        ),
        migrations.AlterField(
            model_name='comanda',
            name='telefon',
            field=models.CharField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='datanasterii',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nr_puncte',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
