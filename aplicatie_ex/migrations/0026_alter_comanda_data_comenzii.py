# Generated by Django 5.1 on 2024-12-19 00:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0025_remove_comanda_datacreare_remove_comanda_id_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='data_comenzii',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
