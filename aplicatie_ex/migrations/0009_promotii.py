# Generated by Django 5.1 on 2024-12-02 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0008_vizualizari'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotii',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=20, unique=True)),
                ('data_creare', models.DateField(null=True)),
                ('data_expirare', models.DateField(null=True)),
                ('reducere', models.FloatField()),
                ('tip_promotie', models.CharField(choices=[('discount', 'Discount'), ('cadou', 'Cadou'), ('aniversare', 'Aniversare')], max_length=20)),
            ],
        ),
    ]
