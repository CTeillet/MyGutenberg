from django.core.management import BaseCommand

from books.models import IndexWords, JaccardDistance


def get_index(i):
    """Create the the list of index words from the books i and return the list of index words from the books i."""
    return list(IndexWords.objects.filter(idBook=i).values_list('idWord', 'count'))


def jaccard_distance(list1, idBook1, list2, idBook2):
    """Calculate the Jaccard distance between two lists of words."""
    words_1 = set(map(lambda x: x[0], list1))
    words_2 = set(map(lambda x: x[0], list2))
    words_union = words_1.union(words_2)
    top = 1
    bottom = 1
    for word in words_union:
        nb_word_book1 = find_nb(idBook1, word)
        nb_word_book2 = find_nb(idBook2, word)
        top += max(nb_word_book1, nb_word_book2) - min(nb_word_book1, nb_word_book2)
        bottom += max(nb_word_book1, nb_word_book2)
    return int(top / bottom * 100)


def find_nb(idBook, idWord):
    """Find the number of occurrences of the word in the book."""
    try:
        res = IndexWords.objects.get(idBook=idBook, idWord=idWord).count
    except IndexWords.DoesNotExist:
        res = 0
    return res


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Create the Jaccard distance between all the books that are not already in the Jaccard table and are indexed.
        """
        print('create Jaccard Distance')

        idBook1 = 1
        idBook2 = 100
        index1 = get_index(idBook1)
        index2 = get_index(idBook2)
        res = jaccard_distance(index1, idBook1, index2, idBook2)
        JaccardDistance.objects.create(idBook1=idBook1, idBook2=idBook2, distance=res)
        print(res)
