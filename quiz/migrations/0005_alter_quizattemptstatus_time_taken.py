# Generated by Django 3.2.3 on 2021-05-30 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quizattemptstatus_current_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattemptstatus',
            name='time_taken',
            field=models.IntegerField(default=0),
        ),
    ]
