from django.db import models

class Work(models.Model):
    """Work: Each piece of music work"""

    title = models.CharField(max_length=250, null=False, default='UNTITLED')
    contributors = models.ManyToManyField('Contributor', related_name='contributors', blank=True)
    iswc = models.CharField(max_length=20, null=False)

    def __str__(self):
            return self.iswc


class Contributor(models.Model):
    """Contributor: Name of song contributors, used as a ManyToManyField in  Work"""

    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Source(models.Model):
    """Source: Name of each label and the ID the song has in it"""

    name = models.CharField(max_length=100, null=False)
    id_source = models.IntegerField(null=False)
    work = models.ForeignKey(Work, related_name='sources', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
            return 'ID:' + str(self.id_source) + ' LABEL:' + self.name