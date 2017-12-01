from library.models import Edition
import re
import requests
import os
import json
from django.conf import settings

DIR = os.path.dirname(os.path.abspath(__file__))

def process_edition(edition):
    r = requests.get(edition.source)
    if r.status_code == requests.codes.ok:
        filename = re.sub(r"[^a-zA-Z0-9.-]", "_", edition.identifier)
        edpath = os.path.join(DIR, "data", edition.org, filename)
        if not os.path.exists(edpath):
            os.makedirs(edpath)
        # Copy the source
        path = os.path.join(edpath, "%s.xml" % filename)
        f = open(path, 'w')
        f.write(r.text)
        f.close
        # Just load the file into exist. Queries will give us TOC, position metadata, etc.
        # URL like http://localhost:8088/rest/db/LDLT/SCS/urn_cts_latinLit_phi0830.phi001.dll_1.xml
        url = "%srest/db/LDLT/%s/%s.xml" % (settings.EXIST_URL, edition.org, filename)
        r = requests.put(url, data=open(path).read().encode('utf-8'), auth=('admin',''))
        if r.status_code == requests.codes.created:
            url = "%sapps/CTXQ/toc/LDLT/%s/d/%s/" % (settings.EXIST_URL, edition.org, filename)
            toc = requests.get(url)
            edition.sections = toc.text
            edition.save()
            toc = json.loads(toc.text)
            for part in toc['item']:
                with open(edition.file(part['id']), 'w') as f:
                    r = requests.get("%sapps/CTXQ/ce/LDLT/%s/d/%s/i/%s" % (settings.EXIST_URL, edition.org, filename, part['id']))
                    f.write(r.text)
        else:
            raise ValueError("Could not save source to the database. Status code: %s." % (r.status_code))
    else:
        raise ValueError("Could not retrieve source from %s" % edition.source)
