# Generated by Django 5.1.7 on 2025-04-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='123', max_length=32, verbose_name='Телефон'),
        ),
    ]
