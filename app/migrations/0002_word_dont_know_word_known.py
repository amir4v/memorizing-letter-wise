# Generated by Django 4.2 on 2024-06-26 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="dont_know",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="word",
            name="known",
            field=models.IntegerField(default=0),
        ),
    ]
