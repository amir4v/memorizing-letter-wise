import json
dictionary = json.load(open('./dictionary.json', 'rt'))
_dictionary = {}
for k, v in dictionary.items():
    _dictionary[k.lower()] = v
dictionary = _dictionary

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from app.models import Word

for k, v in dictionary.items():
    word, created = Word.objects.get_or_create(word=k)
    word.definition = v
    word.save()
