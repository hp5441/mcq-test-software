# Generated by Django 3.2.3 on 2021-05-30 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_quizattemptstatus_time_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerstatus',
            name='correctness',
            field=models.BooleanField(default=True),
        ),
    ]
