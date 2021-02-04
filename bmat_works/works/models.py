from django.db import models

# Create your models here.
class Work(models.Model):
    title = models.CharField(max_length=250, null=False, default='UNTITLED')
    contributors = models.ManyToManyField('Contributor', related_name='contributors', blank=True)
    iswc = models.CharField(max_length=20, null=True)
    sources = models.ManyToManyField('Source', related_name='labels', blank=True)


class Contributor(models.Model):
    name = models.CharField(max_length=100, null=False)


class Source(models.Model):
    name = models.CharField(max_length=100, null=False)