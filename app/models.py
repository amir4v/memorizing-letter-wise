from django.db import models


class Word(models.Model):
    word = models.TextField(null=False, blank=False, unique=True, db_index=True)
    
    # from mymemory.translated: https://api.mymemory.translated.net/get?q={word}&langpair=en|fa
    mymemory_translated_fas = models.TextField()
    
    # from dictionaryapi: https://api.dictionaryapi.dev/api/v2/entries/en/{word}
    dictionaryapi_json = models.TextField()
    dictionaryapi_yaml = models.TextField()
    dictionaryapi_phonetics = models.TextField()
    dictionaryapi_definitions = models.TextField()
    dictionaryapi_synonyms = models.TextField()
    dictionaryapi_antonyms = models.TextField()
    
    nltk_synonyms = models.TextField() # from the nltk library
    nltk_antonyms = models.TextField() # from the nltk library
    
    # these are made-up
    letterized_1 = models.TextField()
    letterized_2 = models.TextField()
    letterized_3 = models.TextField()
    
    batch_definitions = models.TextField() # from a dictionary.json file
    nltk_definitions = models.TextField() # from the nltk library
    nltk_examples = models.TextField() # from the nltk library
    
    google_translation = models.TextField() # https://translate-pa.googleapis.com/v1/translate?params.client=gtx&query.source_language=auto&query.target_language=fa&query.display_language=en-US&query.text={text}&key=AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA&data_types=TRANSLATION&data_types=SENTENCE_SPLITS&data_types=BILINGUAL_DICTIONARY_FULL
