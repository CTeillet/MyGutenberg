from django.db import models


# Create your models here.
class Book(models.Model):
    gutenbergID = models.IntegerField(default='-1', primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    downloaded = models.BooleanField(default=False)
    download_link = models.CharField(max_length=255, default='')
    indexed = models.BooleanField(default=False)

    class Meta:
        ordering = ('gutenbergID',)

    def __str__(self):
        return self.title


class Words(models.Model):
    word = models.CharField(max_length=255)

    class Meta:
        ordering = ('word',)

    def __str__(self):
        return self.word


class IndexWords(models.Model):
    idWord = models.ForeignKey(Words, on_delete=models.CASCADE)
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ('idBook',)
        unique_together = ('idWord', 'idBook')

    def __str__(self):
        return self.idWord.word


class BlacklistWords(models.Model):
    word = models.CharField(max_length=255, primary_key=True)

    class Meta:
        ordering = ('word',)

    def __str__(self):
        return self.word


class JaccardDistance(models.Model):
    idBook1 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book1')
    idBook2 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book2')
    distance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('idBook1', 'idBook2')

    def __str__(self):
        return str(self.idBook1) + ' - ' + str(self.idBook2)


class ClickedBook(models.Model):
    idBook = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ('idBook',)
        unique_together = ('idBook',)

    def __str__(self):
        return self.idBook.title

