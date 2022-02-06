from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from django.http import JsonResponse
from iso639 import Lang
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core import serializers
from books.models import Book, Words, IndexWords
from books.serializers import BookSerializer
from research_RegEx.regex import generate_dfa


class BooksView(APIView):
    def get(self, request):
        res = serializers.serialize('json', Book.objects.filter(downloaded=True), cls=LazyEncoder)
        return JsonResponse(res, safe=False)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return str(obj)
        return super().default(obj)


class SearchBook(APIView):
    def get(self, request, word_req):
        res_words = Words.objects.filter(word=word_req)  # index of the word in the table Words
        res = set()
        for word in res_words:
            res_word = IndexWords.objects.filter(idWord_id=word.id)  # id of the book that contains the word
            for indexWord in res_word:
                b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                res.add(b)
        json = BookSerializer(res, many=True).data
        return Response(json)


class SearchBookByLanguage(APIView):
    def get(self, request, language):
        res = Book.objects.filter(language=language, downloaded=True)
        json = BookSerializer(res, many=True).data
        return Response(json)


class AdvancedSearchBook(APIView):
    def get(self, request, expression):
        if contains_only_letters_or_digit(expression):
            res_words = Words.objects.filter(word__contains=expression)  # id of the words that contain the word
            res = set()
            for word in res_words:
                res_word = IndexWords.objects.filter(idWord_id=word.id)  # id of the book that contains the word
                for indexWord in res_word:
                    b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                    res.add(b)
            json = BookSerializer(res, many=True).data
            return Response(json)
        else:
            words = list(Words.objects.values_list('word', flat=True))
            dfa = generate_dfa(expression)
            res = set()
            for word in words:
                if dfa.apply(word):
                    res_word = IndexWords.objects.filter(idWord_id=word)
                    for indexWord in res_word:
                        b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                        res.add(b)
            json = BookSerializer(res, many=True).data
            return Response(json)


def contains_only_letters_or_digit(word):
    for c in word:
        if not c.isalpha() and not c.isdigit():
            return False
    return True


class AddBookClick(APIView):
    def post(self, request, book_id):
        book = Book.objects.get(gutenbergID=book_id)
        book.clicks += 1
        book.save()
        return Response({'clicks': book.clicks})


class SearchByTitle(APIView):
    def get(self, request):
        title_req = request.GET.get('title')
        res = Book.objects.filter(title__contains=title_req)
        json = BookSerializer(res, many=True).data
        return Response(json)


class LanguageView(APIView):
    def get(self, request):
        languages_list = Book.objects.values_list('language', flat=True).distinct().order_by()
        print(languages_list)
        res_list = []
        for language in languages_list:
            lang = Lang(language)
            res_list.append((lang.name, language))
        return Response(res_list)


class ShowBook(APIView):
    def get(self, request, book_id):
        book = Book.objects.get(gutenbergID=book_id)
        json = BookSerializer(book).data
        return Response(json)


class SearchBookLanguage(APIView):
    def get(self, request, word_req, lang):
        res_words = Words.objects.filter(word=word_req)  # index of the word in the table Words
        res = set()
        for word in res_words:
            res_word = IndexWords.objects.filter(idWord_id=word.id)  # id of the book that contains the word
            for indexWord in res_word:
                b = Book.objects.get(gutenbergID=indexWord.idBook_id, language=lang)
                res.add(b)
        json = BookSerializer(res, many=True).data
        return Response(json)