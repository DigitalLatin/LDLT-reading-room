from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Edition
import json
import objectpath
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
        edition = Edition.objects.get(identifier=id)
        # URL like /CTXQ/ce/<collection>/d/<document_id>/i/<node_id>
        sections = objectpath.Tree(json.loads(edition.sections))
        found = prev = next = None
        start = sections.execute("$..item[0].ref.target")[1:]
        if part:
            i = 0
            for section in sections.execute("$..item"):
                if section["ref"]["target"][1:] == part:
                    found = True
                    print("Found %s at index %s" % (part, i))
                if not found:
                    i = i + 1
            if i > 0:
                prev = sections.execute("$..item[%s]" % str(i-1))["ref"]["target"][1:]
            if i < sections.execute("len($..item)") - 1:
                next = sections.execute("$..item[%s]" % str(i+1))["ref"]["target"][1:]
            parttype = sections.execute("$..item[%s]" % str(i))["ref"]["n"]
        else:
            part = sections.execute("$..item[0]")["ref"]["target"][1:]
            parttype = sections.execute("$..item[0]")["ref"]["n"]
            next = sections.execute("$..item[1]")["ref"]["target"][1:]
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
