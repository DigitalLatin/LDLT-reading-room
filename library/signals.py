from library.models import Edition
from library.utilities import process_edition
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Edition)
def load_edition(sender, instance=None, **kwargs):
    if not instance:
        return
    if hasattr(instance, "_dirty"):
        return

    try:
        instance._dirty = True
        process_edition(instance)
    finally:
        del instance._dirty
