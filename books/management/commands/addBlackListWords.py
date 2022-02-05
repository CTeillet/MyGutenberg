from django.core.management import BaseCommand
from django.db import IntegrityError

from books.models import BlacklistWords


class Command(BaseCommand):
    help = 'Create index for search'

    def handle(self, *args, **options):
        print("Creating Blacklist Words")

        with open("ressources/blacklist_words.txt") as f:
            print("Reading file")
            lines = f.readlines()
            for line in lines:
                word = line.strip()
                print("Adding word: " + word)
                try:
                    BlacklistWords.objects.create(word=word)
                except IntegrityError:
                    print("Word already in database")
        print("Blacklist Words created")
