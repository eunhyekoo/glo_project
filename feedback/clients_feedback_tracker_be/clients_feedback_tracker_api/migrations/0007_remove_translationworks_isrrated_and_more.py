# Generated by Django 4.0.2 on 2022-05-30 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients_feedback_tracker_api', '0006_translationsentences_sourcesentence_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translationworks',
            name='isRrated',
        ),
        migrations.AddField(
            model_name='contenttitles',
            name='isRrated',
            field=models.BooleanField(default=False),
        ),
    ]
