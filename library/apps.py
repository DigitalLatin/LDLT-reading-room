from django.apps import AppConfig

class LibraryConfig(AppConfig):
    name = 'library'

    def ready(self):
        import library.signals
        import requests
        r = requests.get("http://localhost:8088/exist/rest/")
        if r.status_code != requests.codes.ok:
            raise SystemExit("eXist database not available.")
