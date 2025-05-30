# Generated by Django 5.1 on 2024-12-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0010_mancare_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotii',
            name='data_creare',
            field=models.DateField(blank=True, default='2021-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='promotii',
            name='data_expirare',
            field=models.DateField(blank=True, default='2021-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='promotii',
            name='nume',
            field=models.CharField(blank=True, default='Promotie', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='promotii',
            name='reducere',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
