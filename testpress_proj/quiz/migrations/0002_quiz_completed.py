# Generated by Django 3.2.3 on 2021-05-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]
