from django.db import models


# Create your models here.
class Book(models.Model):
    gutenbergID = models.IntegerField(default='-1')
    title = models.CharField(max_length=255)
    desc = models.TextField()
    language = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('gutenbergID',)

    def __str__(self):
        return self.title
