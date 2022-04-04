# Generated by Django 3.2.9 on 2022-03-25 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0016_teacher_notification_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher_leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=80)),
                ('message', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS.teacher')),
            ],
        ),
    ]