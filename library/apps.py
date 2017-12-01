from django.apps import AppConfig
from django.conf import settings

class LibraryConfig(AppConfig):
    name = 'library'

    def ready(self):
        import library.signals
        import requests
        r = requests.get("%srest/" % settings.EXIST_URL)
        if r.status_code != requests.codes.ok:
            raise SystemExit("eXist database not available.")
