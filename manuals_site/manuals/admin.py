from django.contrib import admin
from .models import Manual, Directory
from mptt.admin import MPTTModelAdmin

admin.site.register(Manual)
admin.site.register(Directory, MPTTModelAdmin)
