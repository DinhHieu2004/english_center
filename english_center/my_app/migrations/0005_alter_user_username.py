# Generated by Django 5.1.1 on 2024-11-11 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_alter_user_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
