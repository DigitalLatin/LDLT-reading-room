from django.shortcuts import render
from django.http import HttpResponse
from .models import Edition, Part
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def index(request):
    editions = Edition.objects.filter(active=True)
    return render(request, 'library/index.html', {'editions': editions})

def edition(request, id, part=None):
    try:
        print(id)
        edition = Edition.objects.get(identifier=id)
        if part:
            section = Part.objects.get(parent_id=edition.id, xml_id=part)
            f = open(os.path.join(DIR, "data", re.sub(r"[^a-zA-Z0-9.-]", "_", edition.identifier), part), "r")
            text = f.read()
            f.close()
            sections = edition.part_set.all()
            if section.order > 0:
                prev = sections[section.order - 1]
            else:
                prev = None
            if section.order < sections.count() - 1:
                next = sections[section.order + 1]
            else:
                next = None
        else:
            part = 'front'

    except Edition.DoesNotExist:
        raise Http404("Edition %s not found" % id)
    return render(request, 'library/edition.html', {'edition': edition, 'part': part, 'text': text, 'prev': prev, 'next': next})
