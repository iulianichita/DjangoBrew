# Generated by Django 5.1 on 2024-11-24 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0003_customuser_locatie_fav'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nr_puncte',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
