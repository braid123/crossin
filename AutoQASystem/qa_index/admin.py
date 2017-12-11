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


class CommentAdmin(ImportExportModelAdmin):
    list_display = ('qaitem', 'content')
    search_fields = ('qaitem', 'content')
    fieldsets = (
        ['Main', {
            'fields': ('qaitem', 'content')
        }],
    )


admin.site.register(QAItem, QAItemAdmin)
admin.site.register(Comment, CommentAdmin)