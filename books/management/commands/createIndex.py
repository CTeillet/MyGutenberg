from django.core.management import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Create index for search'

    def handle(self, *args, **options):
        print("Creating index")
        bs = Book.objects.filter(downloaded=True, indexed=False)
        for b in bs:
            f = open("/tmp/ebooks/{}.txt".format(b.gutenbergID), 'w').close()



            b.indexed = True
            b.save()
        print("Index created")
