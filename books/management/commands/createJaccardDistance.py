from django.core.management import BaseCommand
from concurrent.futures import ThreadPoolExecutor

from books.models import IndexWords, JaccardDistance, Book


def get_index(i):
    """Create the the list of index words from the books i and return the list of index words from the books i."""
    # Select idWord, count from IndexWords where idBook = i;
    return list(IndexWords.objects.filter(idBook=i).values_list('idWord', 'count'))


def jaccard_distance(list1, list2):
    """Calculate the Jaccard distance between two lists of words."""
    dict_words = dict()  # Dictionnary of the words
    for (word, count) in list1:
        dict_words[word] = (count, 0)
    for (word, count) in list2:
        if word in dict_words:
            dict_words[word] = (max(dict_words[word][0], count), min(dict_words[word][0], count))
        else:
            dict_words[word] = (count, 0)
    top = 1
    bottom = 1
    for word, (nb_word_book1, nb_word_book2) in dict_words:
        top += nb_word_book1 - nb_word_book2
        bottom += nb_word_book1
    return int(top / bottom * 100)


def traitement(i, j):
    print(i, j)
    book1 = Book.objects.get(gutenbergID=i)
    book2 = Book.objects.get(gutenbergID=j)
    jaccard_distance_i_j = jaccard_distance(get_index(i), get_index(j))
    print('{} - {} : {}'.format(i, j, jaccard_distance_i_j))
    JaccardDistance(idBook1=book1, idBook2=book2, distance=jaccard_distance_i_j).save()
    print('Jaccard distance between book {} and {} is {}'.format(i, j, jaccard_distance_i_j))


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Create the Jaccard distance between all the books that are not already in the Jaccard table and are indexed.
        """
        print('create Jaccard Distance')
        books = IndexWords.objects.values_list('idBook', flat=True).distinct()
        paires_max = [(i, j) for i in books for j in books if i < j]
        paires_exist = JaccardDistance.objects.values_list('idBook1', 'idBook2').distinct()
        paires_to_create = [paire for paire in paires_max if paire not in paires_exist]
        print(len(books))
        with ThreadPoolExecutor(max_workers=12) as executor:
            for i, j in paires_to_create:
                executor.submit(traitement, i, j)
        print('Jaccard distance created')
