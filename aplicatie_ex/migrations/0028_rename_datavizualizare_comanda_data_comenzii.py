# Generated by Django 5.1 on 2024-12-19 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0027_remove_comanda_data_comenzii_comanda_datavizualizare'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comanda',
            old_name='datavizualizare',
            new_name='data_comenzii',
        ),
    ]
