# Generated by Django 4.0.2 on 2022-06-10 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients_feedback_tracker_api', '0007_remove_translationworks_isrrated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='errortypes',
            name='negativeSeverityScore',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='errortypes',
            name='positiveSeverityScore',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contenttitles',
            name='workType',
            field=models.CharField(choices=[('webtoon', 'Webtoon'), ('webnovel', 'Webnovel')], default='webtoon', max_length=10, null=True),
        ),
    ]