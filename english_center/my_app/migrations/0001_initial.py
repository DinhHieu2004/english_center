# Generated by Django 5.1.1 on 2024-12-10 16:21

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('level', models.CharField(choices=[('a1', 'A1'), ('a2', 'A2'), ('b1', 'B1'), ('b2', 'B2')], max_length=2)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('total_session', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PlacementTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(help_text='Thời gian làm bài (phút)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(blank=True, max_length=30)),
                ('username', models.CharField(blank=True, max_length=20, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('join_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FinalExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(help_text='Thời gian làm bài (phút)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(choices=[('a1', 'A1'), ('a2', 'A2'), ('b1', 'B1'), ('b2', 'B2')], max_length=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_exams', to='my_app.course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audio/')),
                ('choice_a', models.TextField(blank=True, default=' ', max_length=200, null=True)),
                ('choice_b', models.CharField(blank=True, default=' ', max_length=200, null=True)),
                ('choice_c', models.TextField(blank=True, default=' ', max_length=200, null=True)),
                ('choice_d', models.TextField(blank=True, default=' ', max_length=200, null=True)),
                ('correct_answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, null=True)),
                ('level', models.CharField(choices=[('a1', 'A1'), ('a2', 'A2'), ('b1', 'B1'), ('b2', 'B2')], max_length=2)),
                ('final_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='my_app.finalexam')),
                ('placement_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='my_app.placementtest')),
            ],
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.course')),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('revenue', 'Revenue'), ('student', 'Student'), ('teacher', 'Teacher'), ('course', 'Course')], max_length=50)),
                ('data', models.JSONField()),
            ],
            options={
                'ordering': ['-date', 'type'],
                'unique_together': {('date', 'type')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_studying', models.BooleanField(default=False)),
                ('level', models.CharField(choices=[('none', 'Chưa xác định'), ('a1', 'A1'), ('a2', 'A2'), ('b1', 'B1'), ('b2', 'B2')], default='none', max_length=10)),
                ('has_taken_test', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('final_test_passed', models.BooleanField(null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.student')),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(through='my_app.CourseEnrollment', to='my_app.student'),
        ),
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
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('exam_type', models.CharField(choices=[('final', 'Final Exam'), ('placement', 'Placement Test')], default='placement', max_length=10)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='my_app.question')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='my_app.student')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(choices=[('bachelor', 'Cử nhân'), ('master', 'Thạc sĩ'), ('phd', 'Tiến sĩ')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_app.teacher'),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(choices=[('placement', 'Placement Test'), ('final', 'Final Exam')], max_length=10)),
                ('score', models.FloatField()),
                ('level', models.CharField(choices=[('a1', 'A1'), ('a2', 'A2'), ('b1', 'B1'), ('b2', 'B2')], max_length=2)),
                ('total_questions', models.IntegerField()),
                ('correct_answers', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results', to='my_app.student')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(0, 'Thứ 2'), (1, 'Thứ 3'), (2, 'Thứ 4'), (3, 'Thứ 5'), (4, 'Thứ 6'), (5, 'Thứ 7'), (6, 'Chủ nhật')])),
                ('start_time', models.TimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='my_app.course')),
            ],
            options={
                'ordering': ['weekday', 'start_time'],
                'unique_together': {('course', 'weekday')},
            },
        ),
    ]
