from django.db import models


class Word(models.Model):
    """
    select * from app_word where tidk != 0 order by tidk desc;
    """
    
    word = models.TextField(null=False, blank=False, unique=True, db_index=True)
    
    # How many times i didn't know?
    tidk = models.IntegerField(default=0)
    
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
    
    @property
    def phonetics(self):
        self.dictionaryapi_phonetics
    
    @property
    def synonyms(self):
        return self.dictionaryapi_synonyms.split(' . ') + self.nltk_synonyms.split(', ')
    
    @property
    def antonyms(self):
        return self.dictionaryapi_antonyms.split(' . ') + self.nltk_antonyms.split(', ')
    
    @property
    def definitions(self):
        return self.dictionaryapi_definitions.split(' . ') + self.nltk_definitions.split(' . ') + self.batch_definitions.split('\n\n')
    
    @property
    def persian(self):
        return self.google_translation.split(' . ') + self.mymemory_translated_fas.split(' . ')
