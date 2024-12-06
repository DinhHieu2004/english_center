# Generated by Django 5.1.1 on 2024-12-04 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_alter_question_choice_a_alter_question_choice_b_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1000000.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='is_studying',
            field=models.BooleanField(default=False),
        ),
    ]