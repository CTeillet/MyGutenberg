import requests
from django.core.management import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Download books from the Gutenberg Project'

    def handle(self, *args, **options):
        print('Downloading books...')
        bs = Book.objects.filter(downloaded=False)
        nb_books_downloaded = len(Book.objects.filter(downloaded=True))
        i = 0
        while nb_books_downloaded + i < 4000:
            self.download_book(bs[i])
            i += 1

    def download_book(self, book):
        r = requests.get(book.download_link, stream=True)
        open('ressources/ebooks/' + str(book.gutenbergID) + '.txt', 'wb').write(r.content)
        book.downloaded = True
        book.save()
