# Generated by Django 5.1.7 on 2025-04-11 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_deleted_at_user_is_deleted_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, default='+7', max_length=32, null=True, verbose_name='Телефон'),
        ),
    ]
