# Generated by Django 5.1.1 on 2024-12-06 09:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_course_price_student_is_studying'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='my_app.course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.teacher')),
            ],
        ),
    ]
