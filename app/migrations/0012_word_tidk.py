# Generated by Django 4.2 on 2024-08-18 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_word_google_translation"),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="tidk",
            field=models.IntegerField(default=0),
        ),
    ]
