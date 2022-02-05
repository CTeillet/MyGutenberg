from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from iso639 import languages
from rest_framework.views import APIView

from django.core import serializers
from books.models import Book, Words, IndexWords
from research_RegEx.regex import generate_dfa


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
        res_words = Words.objects.filter(word=word_req)  # index of the word in the table Words
        res = set()
        for word in res_words:
            res_word = IndexWords.objects.filter(idWord_id=word.id)  # id of the book that contains the word
            for indexWord in res_word:
                b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                res.add(b)
        json = serializers.serialize('json', res, cls=LazyEncoder)
        return JsonResponse(json, safe=False)


class SearchBookByLanguage(APIView):
    def get(self, request):
        language_req = request.GET.get('language')
        res = Book.objects.filter(language=language_req)
        json = serializers.serialize('json', res, cls=LazyEncoder)
        return JsonResponse(json, safe=False)


class AdvancedSearchBook(APIView):
    def get(self, request):
        expression = request.GET.get('expression')
        if contains_only_letters_or_digit(expression):
            res_words = Words.objects.filter(word__contains=expression)  # id of the words that contain the word
            res = set()
            for word in res_words:
                res_word = IndexWords.objects.filter(idWord_id=word.id)  # id of the book that contains the word
                for indexWord in res_word:
                    b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                    res.add(b)
            json = serializers.serialize('json', res, cls=LazyEncoder)
            return JsonResponse(json, safe=False)

        else:
            words = list(Words.objects.values_list('word', flat=True))
            dfa = generate_dfa(expression)
            res = set()
            for word in words:
                if dfa.accept(word):
                    res_word = IndexWords.objects.filter(idWord_id=word)
                    for indexWord in res_word:
                        b = Book.objects.get(gutenbergID=indexWord.idBook_id)
                        res.add(b)
            json = serializers.serialize('json', res, cls=LazyEncoder)
            return JsonResponse(json, safe=False)


def contains_only_letters_or_digit(word):
    for c in word:
        if not c.isalpha() and not c.isdigit():
            return False
    return True


class AddBookClick(APIView):
    def post(self, request):
        id_book = request.GET.get('id')
        book = Book.objects.get(gutenbergID=id_book)
        book.clicks += 1
        book.save()
        return JsonResponse({'clicks': book.clicks})


class SearchByTitle(APIView):
    def get(self, request):
        title_req = request.GET.get('title')
        res = Book.objects.filter(title__contains=title_req)
        json = serializers.serialize('json', res, cls=LazyEncoder)
        return JsonResponse(json, safe=False)


class LanguageView(APIView):
    def get(self, request):
        languages_list = Book.objects.values_list('language', flat=True).distinct()
        res_list = []
        for language in languages_list:
            res_list.append((languages.get(language=language).name, language))
        res = serializers.serialize('json', res_list, cls=LazyEncoder)
        return JsonResponse(res, safe=False)
