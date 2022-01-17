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

    class Meta:
        ordering = ('gutenbergID',)

    def __str__(self):
        return self.title
