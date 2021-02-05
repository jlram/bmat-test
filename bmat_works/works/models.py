from django.db import models

# Create your models here.
class Work(models.Model):
    title = models.CharField(max_length=250, null=False, default='UNTITLED')
    contributors = models.ManyToManyField('Contributor', related_name='contributors', blank=True)
    iswc = models.CharField(max_length=20, null=True)

    def __str__(self):
            return self.iswc


class Contributor(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=100, null=False)
    id_source = models.IntegerField(null=False)
    work = models.ForeignKey(Work, related_name='sources', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
            return 'ID:' + str(self.id_source) + ' LABEL:' + self.name