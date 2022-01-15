import pycountry
import requests
from django.core.management import BaseCommand
import feedparser
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Update books'

    def handle(self, *args, **options):
        print('Updating books...')
        rss_url = "https://gutenberg.org/cache/epub/feeds/today.rss"
        news_feed = feedparser.parse(rss_url)
        countries = [country.name for country in pycountry.countries]
        #for entry in news_feed.entries:
        entry = news_feed.entries[0]
        r = requests.get(entry.link)
        #print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        res = soup.find_all(typeof="pgterms:ebook")
        print(res)
