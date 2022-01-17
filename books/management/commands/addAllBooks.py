from django.core.management import BaseCommand
import requests
import tarfile
import xml.etree.ElementTree as et

from django.db import IntegrityError

from books.models import Book


class Command(BaseCommand):
    help = 'Update books'

    def handle(self, *args, **options):
        print('Updating books...')
        url = 'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
        print('Downloading Data...')
        r = requests.get(url, allow_redirects=True)
        print('Saving Data...')
        open('temp/rdf-files.tar.bz2', 'wb').write(r.content)
        print('Reading Data...')
        tar = tarfile.open('temp/rdf-files.tar.bz2')
        members = tar.getmembers()
        for member in members:
            if member.name.endswith('.rdf'):
                print('Reading: ' + member.name)
                extracted = tar.extractfile(member)
                print('Parsing: ' + member.name)
                tree = et.parse(extracted)
                ns = {"dcterms": "http://purl.org/dc/terms/", "pgterms": "http://www.gutenberg.org/2009/pgterms/",
                      "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                      'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

                print("Searching for data")
                title = tree.find(".//dcterms:title", ns)
                author = tree.find(".//pgterms:name", ns)
                language = tree.find('.//dcterms:language//rdf:Description//rdf:value', ns)
                issued = tree.find(".//dcterms:issued", ns)
                modified = tree.find(".//dcterms:modified", ns)
                subject = tree.find(".//dcterms:subject//rdf:Description//rdf:value", ns)
                type = tree.find(".//dcterms:type//rdf:Description//rdf:value", ns)
                download_links = tree.findall(".//dcterms:hasFormat//pgterms:file", ns)
                download_link = ''
                for download_link_temp in download_links:
                    link = download_link_temp.attrib['{'+ns['rdf']+'}about']
                    if link.split('.')[-1] == 'txt':
                        download_link = link
                print("Checking Information")
                l = [title, author, language, issued, modified, subject, type]
                for i in range(len(l)):
                    if l[i] is None:
                        l[i] = ''
                    else:
                        l[i] = l[i].text
                if l[-1] != '':
                    continue
                print("Creating Book")
                b = Book(gutenbergID=member.name.split('/')[2], title=l[0], author=l[1],
                         description=l[5], language=l[2], published_at=l[3],
                         created_at=l[4], download_link=download_link)
                print("Saving Book " + member.name.split('/')[2])
                try:
                    b.save()
                except IntegrityError as e:
                    print("Book already exists")
                    pass
        tar.close()
