import string
from concurrent.futures import ThreadPoolExecutor

from django.core.management import BaseCommand

from books.models import Book, Words, IndexWords, BlacklistWords


def traitement(f, b, blacklist):
    print("Reading file")
    index = dict()
    lines = f.readlines()
    for line in lines:
        for word in line.split():
            word = word.translate(str.maketrans('', '', string.punctuation))
            word = word.lower()
            if word not in index:
                index[word] = 1
            else:
                index[word] += 1
    print("Indexing words {}".format(len(index)))
    for word in index:
        if len(word) > 2 and not (word in blacklist):
            w, _ = Words.objects.get_or_create(word=word)
            try:
                IndexWords.objects.create(idBook=b, idWord=w, count=index[word])
            except:
                pass
    print("Indexing done")
    b.indexed = True
    b.save()
    f.close()
    print("Indexed: {}".format(b.title))


class Command(BaseCommand):
    help = 'Create index for search'

    def handle(self, *args, **options):
        print("Creating index")
        bs = Book.objects.filter(downloaded=True, indexed=False)
        print(bs)
        blacklist = set(BlacklistWords.objects.all().values_list('word', flat=True))
        print("Blacklist: {}".format(blacklist))
        #with ThreadPoolExecutor(max_workers=12) as executor:
        for b in bs:
            print("Indexing book: {}".format(b.title))
            f = open("ressources/ebooks/{}.txt".format(b.gutenbergID), 'r', encoding="utf8")
            #executor.submit(traitement, f, b, blacklist)
            traitement( f, b, blacklist)
        print("Index created")
