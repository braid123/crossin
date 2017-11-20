from django.contrib import admin
from .models import StudentGroup
# Register your models here.
from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
import json


class StudentGroupAdmin(ImportExportModelAdmin):
    # resource_class = LabUsersResource
    # inlines = [InfoQInline, InfoAInline, PaperInline, DialogInline]
    list_display = ('group_name', 'create_time', 'group_note')
    search_fields = ('group_name', 'create_time', 'group_note')
    fieldsets = (
        ['Main', {
            'fields': ('group_name', 'group_note')
        }],
    )

admin.site.register(StudentGroup, StudentGroupAdmin)

