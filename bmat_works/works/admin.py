from django.contrib import admin
from .models import Work, Contributor, Source

# Register your models here.
admin.site.register(Work)
admin.site.register(Contributor)
admin.site.register(Source)