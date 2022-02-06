from rest_framework.serializers import ModelSerializer

from books.models import Book, Words, IndexWords, BlacklistWords, JaccardDistance, ClickedBook


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class WordsSerializer(ModelSerializer):
    class Meta:
        model = Words
        fields = '__all__'


class IndexWordsSerializer(ModelSerializer):
    class Meta:
        model = IndexWords
        fields = '__all__'


class BlacklistWordsSerializer(ModelSerializer):
    class Meta:
        model = BlacklistWords
        fields = '__all__'


class JaccardDistanceSerializer(ModelSerializer):
    class Meta:
        model = JaccardDistance
        fields = '__all__'


class ClickedBookSerializer(ModelSerializer):
    class Meta:
        model = ClickedBook
        fields = '__all__'
