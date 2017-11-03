from library.models import Edition
import re
import requests
import os

DIR = os.path.dirname(os.path.abspath(__file__))

def process_edition(edition):
    r = requests.get(edition.source)
    if r.status_code == requests.codes.ok:
        filename = re.sub(r"[^a-zA-Z0-9.-]", "_", edition.identifier)
        edpath = os.path.join(DIR, "data", edition.org)
        if not os.path.exists(edpath):
            os.makedirs(edpath)
        # Copy the source
        path = os.path.join(edpath, filename)
        f = open(path, "w")
        f.write(r.text)
        f.close
        # Just load the file into exist. Queries will give us TOC, position metadata, etc.
        # URL like http://localhost:8088/rest/db/LDLT/SCS/urn_cts_latinLit_phi0830.phi001.dll_1.xml
        url = "http://localhost:8080/exist/rest/db/LDLT/%s/%s.xml" % (edition.org, filename)
        r = requests.put(url, data=open(path).read().encode('utf-8'), auth=('admin',''))
        if r.status_code == requests.codes.created:
            url = "http://localhost:8080/exist/apps/CTXQ/toc/LDLT/%s/d/%s/" % (edition.org, filename)
            print(url)
            toc = requests.get(url)
            print(toc)
            edition.sections = toc.text
            edition.save()
        else:
            raise ValueError("Could not save source to the database. Status code: %s." % (r.status_code))
    else:
        raise ValueError("Could not retrieve source from %s" % edition.source)
