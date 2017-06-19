from django.contrib import admin

# Register your models here.
from .models import Edition, Part

admin.site.register(Edition)
admin.site.register(Part)
