# Generated by Django 4.0.2 on 2022-05-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients_feedback_tracker_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="translationsentences",
            name="sentence",
            field=models.TextField(default=""),
        ),
    ]