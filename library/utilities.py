from lxml import etree
from library.models import Edition, Part
import re
import requests
import os

DIR = os.path.dirname(os.path.abspath(__file__))

def process_edition(edition):
    r = requests.get(edition.source)
    if r.status_code == requests.codes.ok:
        xml = etree.XML(r.content)
        transform = etree.XSLT(etree.parse(os.path.join(DIR, "xslt", "make-CETEIcean.xsl")))
        edpath = os.path.join(DIR, "data", re.sub(r"[^a-zA-Z0-9.-]", "_", edition.identifier))
        if not os.path.exists(edpath):
            os.makedirs(edpath)
        if edition.sections:
            ids = edition.sections.split(",")
            i = 0
            for id in ids:
                value = etree.XSLT.strparam(id)
                result = transform(xml, section=value)
                f = open(edpath + "/" + id, "w")
                f.write(str(result))
                f.close()
                part = Part(parent=edition, xml_id=id, label=xml.xpath("id('%s')/@n" % id)[0], order=i)
                part.save()
                i = i + 1
        # Do the whole file as well
        result = transform(xml)
        f = open(os.path.join(edpath, "index"), "w")
        f.write(str(result))
        f.close
        # Copy the source
        f = open(os.path.join(edpath, "source"), "w")
        f.write(r.text)
        f.close
    else:
        raise ValueError("Could not retrieve source from %s" % edition.source)
