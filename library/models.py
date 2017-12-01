from django.db import models
import re
import os

# Create your models here.
class Edition(models.Model):
    identifier = models.CharField(max_length=400)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    ORGS = (
        ("SCS", "Society for Classical Studies"),
        ("MAA", "Medieval Academy of America"),
        ("RSA", "Renaissance Society of America")
    )
    org = models.CharField(max_length=3, choices=ORGS, default="SCS")
    pub_date = models.DateTimeField('date published')
    source = models.URLField(max_length=400)
    custom_css = models.URLField('custom CSS', blank=True)
    custom_js = models.URLField('custom JavaScript', blank=True)
    version = models.CharField(max_length=30)
    replaces = models.CharField(max_length=400, blank=True)
    sections = models.TextField(editable=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def file(self, section):
        DIR = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(DIR, "data", self.org, re.sub(r"[^a-zA-Z0-9.-]", "_", self.identifier), section)
