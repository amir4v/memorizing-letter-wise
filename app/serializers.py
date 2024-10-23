from rest_framework import serializers

from .models import Word


class WordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'word',
            'phonetics',
            'synonyms',
            'antonyms',
            'definitions',
            'persian',
        ]
