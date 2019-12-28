from django.contrib import admin
from .models import Manual, Directory, Department
from mptt.admin import MPTTModelAdmin

admin.site.register(Department)
admin.site.register(Manual)
admin.site.register(Directory, MPTTModelAdmin)
