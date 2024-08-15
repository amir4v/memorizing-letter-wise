import os
import sys
import yaml

import requests as r

def get_fa_translations(word, url='https://api.mymemory.translated.net/get?q=%s&langpair=en|fa'):
    try:
        url = url % word
        res = r.get(url).json()
        matches = res.get('matches', [])
        matches = [item['translation'].strip(' .') for item in matches]
        return (
            True,
            ' . '.join(matches),
        )
    except Exception as e:
        print(e)
        return (
            False,
            '',
        )

def _get_definitions(word, url='https://api.dictionaryapi.dev/api/v2/entries/en/%s'):
    url = url % word
    res = r.get(url)
    raw_json = res.content.decode('utf-8')
    res = res.json()
    raw_yaml = yaml.dump(res)
    
    phonetics = []
    definitions = []
    synonyms = []
    antonyms = []
    
    for item in res:
        phonetic = item.get('phonetic')
        if phonetic:
            phonetics.append(phonetic)
        
        for meaning in item.get('meanings', []):
            _definitions = [definition['definition'] for definition in meaning.get('definitions', [])
                            if definition['definition'] not in ['', None]]
            _synonyms = meaning.get('synonyms')
            _antonyms = meaning.get('antonyms')
            
            if _definitions != []:
                definitions += _definitions
            if _synonyms:
                synonyms += _synonyms
            if _antonyms:
                antonyms += _antonyms
    
    return (
        True,
        ' . '.join(phonetics),
        ' . '.join(definitions),
        ' . '.join(synonyms),
        ' . '.join(antonyms),
        raw_json,
        raw_yaml,
    )

def get_definitions(word, url='https://api.dictionaryapi.dev/api/v2/entries/en/%s'):
    try:
        return _get_definitions(word, url='https://api.dictionaryapi.dev/api/v2/entries/en/%s')
    except Exception as e:
        print(e)
        return (
            False,
            '',
            '',
            '',
            '',
            '',
            '',
        )

# -----------------------------------------------------------------------------

try:
    import os
    import django
    import pyperclip
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    from app.models import Word
except Exception as e:
    print(e)

if len(sys.argv) == 2 and sys.argv[1]:
    _word = word = sys.argv[1]
else:
    _word = word = pyperclip.paste()
word = word.strip().lower()
word = word.strip(' `~!@#$%^&*()_+-=[]{};:\'",<.>/?\\')

def print_word(word):
    print(':The-Word:', f'"{word.word}"', '\n\n')
    print(':nltk-Definitions:', f'"{word.nltk_definitions}"', '\n\n')
    print(':nltk-Synonyms:', f'"{word.nltk_synonyms}"', '\n\n')
    print(':nltk-Antonyms:', f'"{word.nltk_antonyms}"', '\n\n')
    print(':batch-Definitions:', f'"{word.batch_definitions}"', '\n\n')
    print(':nltk-Examples:', f'"{word.nltk_examples}"', '\n\n')
    
    print('<->', '\n\n')
    
    flag_fa, fa_translations = get_fa_translations(word.word)
    flag_en, phonetics, definitions, synonyms, antonyms, raw_json, raw_yaml = get_definitions(word.word)
    flag = flag_fa and flag_en
    word.mymemory_translated_fas = fa_translations
    word.dictionaryapi_phonetics = phonetics
    word.dictionaryapi_definitions = definitions
    word.dictionaryapi_synonyms = synonyms
    word.dictionaryapi_antonyms = antonyms
    word.dictionaryapi_raw_json = raw_json
    word.dictionaryapi_raw_yaml = raw_yaml
    if flag:
        word.save()
    
    print(':mymemory_translated_Fas:', f'"{fa_translations}"', '\n\n')
    print(':dictionaryapi_Phonetics:', f'"{phonetics}"', '\n\n')
    print(':dictionaryapi_Definitions:', f'"{definitions}"', '\n\n')
    print(':dictionaryapi_Synonyms:', f'"{synonyms}"', '\n\n')
    print(':dictionaryapi_Antonyms:', f'"{antonyms}"', '\n\n')
    # print(':dictionaryapi_Raw_JSON:', f'"{raw_json}"', '\n\n')
    # print(':dictionaryapi_Raw_YAML:', f'"{raw_yaml}"', '\n\n')
    
    print('-'*80, '\n\n')

try:
    word, created = Word.objects.get_or_create(word=word)
    print_word(word)
    if created:
        raise Exception('created')
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

word = input('>>>')
os.system(f'python C:/Users/Amir/Desktop/memorizing-letter-wise/translation.py {word}')
