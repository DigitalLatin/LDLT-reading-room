from django.shortcuts import render
from django.http import HttpResponse
from .models import Edition
import json
import os
import re
import requests
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
        # URL like /CTXQ/ce/<collection>/d/<document_id>/i/<node_id>
        doc = re.sub(r"[^a-zA-Z0-9.-]", "_", edition.identifier)
        sections = json.loads(edition.sections)
        print(sections)
        found = prev = next = None
        if part:
            i = 0
            for section in sections["item"]:
                if section["id"] == part:
                    found = True
                    print("Found %s at index %s" % (part, i))
                if not found:
                    i = i + 1
            if i > 0:
                prev = sections["item"][i - 1]["id"]
            if i < len(sections["item"]) - 1:
                next = sections["item"][i + 1]["id"]
        else:
            part = 'titlepage'
            next = sections["item"][1]["id"]
        url = "http://localhost:8080/exist/apps/CTXQ/ce/LDLT/%s/d/%s/i/%s" % (edition.org, doc, part)
        text = requests.get(url).text
        url = "http://localhost:8080/exist/apps/CTXQ/ce/LDLT/%s/d/%s/i/bibliography" % (edition.org, doc)
        bibliography = requests.get(url).text

    except Edition.DoesNotExist:
        raise Http404("Edition %s not found" % id)
    return render(request, 'library/edition.html', {'edition': edition, 'part': part, 'text': text, 'bibliography': bibliography, 'prev': prev, 'next': next})
