from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class DtpResource(resources.ModelResource):
    class Meta:
        model = Dtp

class DtpResource2(resources.ModelResource):
    class Meta:
        model = Dtp_outside

class DtpResource3(resources.ModelResource):
    class Meta:
        model = PiterDtp

class DtpAdmin(ImportExportActionModelAdmin):
    resource_class = DtpResource
    list_display = [field.name for field in Dtp._meta.fields if field.name !="id"]

class DtpAdmin2(ImportExportActionModelAdmin):
    resource_class = DtpResource2
    list_display = [field.name for field in Dtp_outside._meta.fields if field.name !="id"]

class DtpAdmin3(ImportExportActionModelAdmin):
    resource_class = DtpResource3
    list_display = [field.name for field in PiterDtp._meta.fields if field.name !="id"]



admin.site.register(Dtp, DtpAdmin)
admin.site.register(Dtp_outside, DtpAdmin2)
admin.site.register(PiterDtp, DtpAdmin3)
