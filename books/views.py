from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from django.core import serializers
from books.models import Book, Words, IndexWords
from books.serializers import BookSerializer


class BooksView(APIView):
    def get(self, request):
        res = serializers.serialize('json', Book.objects.all(), cls=LazyEncoder)
        return JsonResponse(res, safe=False)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return str(obj)
        return super().default(obj)


class SearchBook(APIView):
    def get(self, request):
        word_req = request.GET.get('word')
        res_words = Words.objects.filter(word__contains=word_req) # id of the words that contain the word
        res = set()
        for word in res_words:
            res_word = IndexWords.objects.filter(idWord_id=word.id) # id of the book that contains the word
            for indexWord in res_word:
                b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                res.add(b)
        json = serializers.serialize('json', res, cls=LazyEncoder)
        return JsonResponse(json, safe=False)

