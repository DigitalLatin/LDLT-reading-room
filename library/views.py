from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Edition
from .utilities import find_items
import json
import os
import re
import requests
import sys

DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def splash(request):
    return render(request, 'library/splash.html')

def about(request):
    return render(request, 'library/about.html')

def index(request):
    editions = Edition.objects.filter(active=True)
    return render(request, 'library/index.html', {'editions': editions})

def edition(request, id, part=None):
    try:
        edition = Edition.objects.get(identifier=id)
        # URL like /CTXQ/ce/<collection>/d/<document_id>/i/<node_id>
        sections = list(find_items(json.loads(edition.sections)))
        found = prev = next = None
        start = sections[0]["ref"]["target"][1:]
        if part:
            i = 0
            for section in sections:
                if section["ref"]["target"][1:] == part:
                    found = True
                if not found:
                    i = i + 1
            if i > 0:
                prev = sections[i-1]["ref"]["target"][1:]
            if i < len(sections) - 1:
                next = sections[i+1]["ref"]["target"][1:]
            parttype = sections[i]["ref"]["n"]
        else:
            part = sections[0]["ref"]["target"][1:]
            parttype = sections[0]["ref"]["n"]
            next = sections[1]["ref"]["target"][1:]
        with open(edition.file(part), encoding="utf-8") as f:
            text = f.read()
        with open(edition.file('bibliography'), encoding="utf-8") as f:
            bibliography = f.read()
        with open(edition.file('toc'), encoding="utf-8") as f:
            toc = f.read()

    except Edition.DoesNotExist:
        raise Http404("Edition %s not found" % id)
    return render(request, 'library/edition.html', {'edition': edition, 'toc': toc, 'part': part, 'parttype': parttype, 'text': text, 'bibliography': bibliography, 'start': start, 'prev': prev, 'next': next})

def add_slash(request):
    return redirect("%s/" % request.path)
