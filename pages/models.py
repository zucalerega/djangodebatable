from django.db import models

# Create your models here.
class Resource(models.Model):
    type = models.CharField(max_length=10, default='null')
    title = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=1000000, default='')
    author = models.CharField(max_length=100, default='')
    published = models.DateTimeField(max_length=100, default='')
    uses = models.IntegerField(default=0)
