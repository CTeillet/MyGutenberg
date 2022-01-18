from django.core.management import BaseCommand

from books.models import Book, BlacklistWords


class Command(BaseCommand):
    help = 'Create index for search'

    def handle(self, *args, **options):
        print("Creating Blacklist Words")

        f = open("/ressources/blacklist_words.txt", 'w')
        for l in f:
            BlacklistWords.objects.create(word=l)
        f.close()
        print("Blacklist Words created")
