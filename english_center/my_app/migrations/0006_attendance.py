# Generated by Django 5.1.1 on 2024-12-06 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_course_price_student_is_studying'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.student')),
            ],
            options={
                'ordering': ['date', 'course', 'student'],
            },
        ),
    ]
