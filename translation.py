try:
    import os
    import django
    import pyperclip
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    from app.models import Word
except Exception as e:
    print(e)

_word = word = pyperclip.paste()
word = word.strip().lower()

def print_word(word):
    print(':The-Word:', f'"{word.word}"', '\n\n')
    print(':Definition:', word.definition, '\n\n')
    print(':Synonyms:', word.synonyms, '\n\n')
    print(':Antonyms:', word.antonyms, '\n\n')
    print(':Examples:', word.examples, '\n\n')
    print(':Definitions:', word.definitions, '\n\n')
    print('-'*80, '\n\n')

try:
    word = Word.objects.get(word=word)
    print_word(word)
except Exception as e:
    try:
        words = Word.objects.filter(word__icontains=word)
        for word in words:
            print_word(word)
        if words.count() <= 0:
            print(f'"{_word}"')
            print(e, 2)
    except Exception as e:
        print(f'"{_word}"')
        print(e, 1)

input('>>>')
