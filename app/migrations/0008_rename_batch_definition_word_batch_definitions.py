# Generated by Django 4.2 on 2024-08-13 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_rename_antonyms_word_nltk_antonyms_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="word",
            old_name="batch_definition",
            new_name="batch_definitions",
        ),
    ]
