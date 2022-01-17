import requests
from django.core.management import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Download books from the Gutenberg Project'

    def handle(self, *args, **options):
        print('Downloading books...')
        bs = Book.objects.filter(downloaded=False)
        for book in bs:
            self.download_book(book)
    def download_book(self, book):
        r = requests.get(book.url, stream=True)
        open('temp/ebooks/'+book.gutenbergID, 'wb').write(r.content)

