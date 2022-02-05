import requests
from django.core.management import BaseCommand

from books.models import Book, ClickedBook


def download_book(book):
    r = requests.get(book.download_link, stream=True)
    open('ressources/ebooks/' + str(book.gutenbergID) + '.txt', 'wb').write(r.content)
    book.downloaded = True
    ClickedBook(idBook=book).save()
    book.save()

class Command(BaseCommand):
    help = 'Download books from the Gutenberg Project'

    def handle(self, *args, **options):
        print('Downloading books...')
        bs = Book.objects.filter(downloaded=False)
        if len(bs) == 0:
            print('No books to download')
        else:
            nb_books_downloaded = len(Book.objects.filter(downloaded=True))
            i = 0
            while nb_books_downloaded + i < 2000:
                print('Downloading book ' + bs[i].title)
                download_book(bs[i])
                i += 1


