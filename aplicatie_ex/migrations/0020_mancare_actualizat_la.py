# Generated by Django 5.1 on 2024-12-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0019_mancare_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='mancare',
            name='actualizat_la',
            field=models.DateField(auto_now=True),
        ),
    ]
