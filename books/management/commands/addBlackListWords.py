from django.core.management import BaseCommand

from books.models import Book, BlacklistWords


class Command(BaseCommand):
    help = 'Create index for search'

    def handle(self, *args, **options):
        print("Creating Blacklist Words")

        with open("ressources/blacklist_words.txt") as f:
            print("Reading file")
            lines = f.readlines()
            print(lines)
            for line in lines:
                print("Adding word: " + line)
                b = BlacklistWords.objects.create(word=line)
                print(b)
        print("Blacklist Words created")
