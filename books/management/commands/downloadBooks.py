from django.core.management import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Download books from the Gutenberg Project'

    def handle(self, *args, **options):
        print('Downloading books...')
        bs = Book.objects.filter(downloaded=False)
        print(len(bs))
        french_books = bs.filter(language='fr')
        print(len(french_books))

