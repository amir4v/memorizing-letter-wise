# Generated by Django 4.2 on 2024-08-13 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_rename_definition_word_batch_definition"),
    ]

    operations = [
        migrations.RenameField(
            model_name="word",
            old_name="antonyms",
            new_name="nltk_antonyms",
        ),
        migrations.RenameField(
            model_name="word",
            old_name="definitions",
            new_name="nltk_definitions",
        ),
        migrations.RenameField(
            model_name="word",
            old_name="examples",
            new_name="nltk_examples",
        ),
        migrations.RenameField(
            model_name="word",
            old_name="synonyms",
            new_name="nltk_synonyms",
        ),
    ]
