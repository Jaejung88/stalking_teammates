# Generated by Django 2.2.4 on 2020-10-21 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj_manage', '0003_project_project_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.CharField(default='Just Start', max_length=45),
        ),
        migrations.AddField(
            model_name='task',
            name='task_urgency',
            field=models.CharField(default='Just Start', max_length=45),
        ),
    ]
