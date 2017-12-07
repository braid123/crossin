from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class QAItemAdmin(ImportExportModelAdmin):
    list_display = ('title', 'desc', 'answer')
    search_fields = ('title', 'desc', 'answer')
    fieldsets = (
        ['Main', {
            'fields': ('title', 'desc', 'answer')
        }],
    )

    def __str__(self):
        return self.title

admin.site.register(QAItem, QAItemAdmin)