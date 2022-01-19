import string

from django.core.management import BaseCommand

from books.models import Book, Words, IndexWords, BlacklistWords


class Command(BaseCommand):
    help = 'Create index for search'

    def handle(self, *args, **options):
        print("Creating index")
        bs = Book.objects.filter(downloaded=True, indexed=False)
        blacklist = BlacklistWords.objects.all()
        for b in bs:
            print("Indexing book: {}".format(b.title))
            with open("ressources/ebooks/{}.txt".format(b.gutenbergID), 'r', encoding="utf8") as f:
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
                print("Indexing words")
                for word in index:
                    if len(word) > 2 and word not in blacklist:
                        w, _ = Words.objects.get_or_create(word=word)
                        IndexWords.objects.create(idBook=b, idWord=w, count=index[word])
                b.indexed = True
                b.save()
                print("Indexed: {}".format(b.title))
        print("Index created")
