import os
import sys
import yaml
import urllib.parse as url_parser

import django
import pyperclip
import requests as r

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from app.models import Word


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
        print(e, 'get_fa_translations')
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
        print(e, 'get_definitions')
        return (
            False,
            '',
            '',
            '',
            '',
            '',
            '',
        )


def get_google_translation(word, url='https://translate-pa.googleapis.com/v1/translate?params.client=gtx&query.source_language=auto&query.target_language=fa&query.display_language=en-US&query.text=%s&key=AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA&data_types=TRANSLATION&data_types=SENTENCE_SPLITS&data_types=BILINGUAL_DICTIONARY_FULL'):
    """
    translation
    sentences
        [
            trans
        ]
    bilingualDictionary
        [
            item
                entry
                    [
                        item
                            word
                            score
                    ]
        ]
    """
    try:
        url = url % url_parser.quote(word, safe='')
        res = r.get(url)
        raw_json = res.content.decode('utf-8')
        res = res.json()
        raw_yaml = yaml.dump(res)
        
        translation = res['translation']
        words = [
            [(inner_word['word'], inner_word.get('score', 0)) for inner_word in word] for word in
            [
                item.get('entry', []) for item in res.get('bilingualDictionary', [])
            ]
        ]
        if words:
            words = words[0]
            words = [word[0] for word in sorted(words, key=lambda x: x[1])]
        else:
            words = [sentence['trans'] for sentence in res.get('sentences', [])]
        words = ' . '.join(words)
        
        # print('translation', translation)
        # print('words', words)
        
        return True, f'{translation} .. {words}'
    except Exception as e:
        print(e, 'get_google_translation')
        return False, ''


def print_word(word):
    print(word.word)
    
    flag_g, google_translation = get_google_translation(word.word)
    if flag_g:
        word.google_translation = google_translation
    
    flag_fa, fa_translations = get_fa_translations(word.word)
    if flag_fa:
        word.mymemory_translated_fas = fa_translations
    
    flag_en, phonetics, definitions, synonyms, antonyms, raw_json, raw_yaml = get_definitions(word.word)
    if flag_en:
        word.dictionaryapi_phonetics = phonetics
        word.dictionaryapi_definitions = definitions
        word.dictionaryapi_synonyms = synonyms
        word.dictionaryapi_antonyms = antonyms
        word.dictionaryapi_raw_json = raw_json
        word.dictionaryapi_raw_yaml = raw_yaml
    
    word.save()


# -----------------------------------------------------------------------------


def fill():
    for word in Word.objects.all().order_by('?'):
        print(word.id, end=' ')
        print_word(word)


fill()
