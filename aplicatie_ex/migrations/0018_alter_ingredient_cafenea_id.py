# Generated by Django 5.1 on 2024-12-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0017_ingredient_cafenea_micdejuns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient_cafenea',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
