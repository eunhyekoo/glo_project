# Generated by Django 4.0.2 on 2022-06-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients_feedback_tracker_api', '0008_errortypes_negativeseverityscore_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttitles',
            name='client',
            field=models.CharField(choices=[('Kakao Ent', 'Kakao'), ('NHN', 'Nhn'), ('Nuon', 'Nuon'), ('Piuri', 'Piuri'), ('Naver Webnovel', 'Naver Webnovel'), ('Tappytoon Webtoon', 'Tappytoon Webtoon'), ('Tappytoon Webnovel', 'Tappytoon Webnovel'), ('Naver Webtoon', 'Naver Webtoon'), ('Tapas', 'Tapas'), ('Naver', 'Naver'), ('KKE', 'Kke'), ('Eineblume', 'Eineblume'), ('StoryX', 'Storyx'), ('Kanafeel', 'Kanafeel'), ('Lezhin', 'Lezhin'), ('Ridi corporation', 'Ridi')], default='Kakao Ent', max_length=20),
        ),
    ]
