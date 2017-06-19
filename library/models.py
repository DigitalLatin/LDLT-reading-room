from django.db import models

# Create your models here.
class Edition(models.Model):
    identifier = models.CharField(max_length=400)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    pub_date = models.DateTimeField('date published')
    source = models.URLField(max_length=400)
    custom_css = models.URLField('custom CSS', blank=True)
    custom_js = models.URLField('custom JavaScript', blank=True)
    version = models.CharField(max_length=30)
    replaces = models.CharField(max_length=400, blank=True)
    sections = models.CharField(max_length=1000, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Part(models.Model):
    parent = models.ForeignKey(Edition, models.CASCADE)
    xml_id = models.CharField('section id', max_length=100)
    label = models.CharField('section number', max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.xml_id + ' (' + str(self.order) + ')'
