# Generated by Django 5.1 on 2024-12-10 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_ex', '0021_customuser_blocat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_block_users', 'Can block or unblock users')]},
        ),
    ]
