# Generated by Django 5.1 on 2024-12-19 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0028_rename_datavizualizare_comanda_data_comenzii'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elev',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=30)),
                ('prenume', models.CharField(max_length=30)),
                ('datanasterii', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valoare', models.IntegerField()),
                ('data_adaugare', models.DateField()),
                ('elev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicatie_ex.elev')),
            ],
        ),
    ]
