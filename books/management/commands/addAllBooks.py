from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Update books'

    def handle(self, *args, **options):
        print('Updating books...')
