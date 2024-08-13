import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from app.models import Word

words = Word.objects.values_list('word', flat=True).all().order_by('id')

open('./words.txt', 'wt').write(
    '\n'.join(words)
)
