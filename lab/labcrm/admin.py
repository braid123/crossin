from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
import json
# Register your models here.


class DialogInline(admin.TabularInline):
    model = Dialog


class AttrOptionInline(admin.TabularInline):
    model = AttrOption


class InfoAInline(admin.TabularInline):
    model = UserInfoA


class InfoQInline(admin.TabularInline):
    model = UserInfoQ


class PaperInline(admin.TabularInline):
    model = Paper


class LabUsersResource(resources.ModelResource):
    """
    用户数据导入导出配置
    """
    id = fields.Field('id', column_name='本站ID')
    user = fields.Field('user', column_name='本站名')
    nickname = fields.Field('nickname', column_name='用户名')
    wechat = fields.Field('wechat', column_name='微信')
    ta = fields.Field('ta', column_name='助教')
    class_id = fields.Field('class_id', column_name='编程教室ID')
    statistic = fields.Field('statistic', column_name='完课统计')
    is_del = fields.Field('is_del', column_name='是否删除')

    def _statistic_format(self, statistic):
        from .views import course_to_status
        statistic_format = {}
        key_replace = dict(LearnedCourse.COURSE_CHOICES)
        value_replace = {j[0]: i for i, j in course_to_status.items()}
        for key, value in statistic.items():
            statistic_format[key_replace[int(key)]] = value_replace[value]
        return statistic_format

    class Meta:
        model = LabUser
        export_order = ('id', 'user', 'nickname', 'wechat', 'class_id', 'ta', 'statistic', 'is_del')

    def dehydrate_user(self, uu):
        return uu.user.username

    def dehydrate_statistic(self, uu):
        statistic = self._statistic_format(json.loads(uu.statistic))
        return '；'.join(['{}: {}'.format(*i) for i in statistic.items()])

    def dehydrate_is_del(self, uu):
        return {0: '否', 1: '是'}[uu.is_del]

# class LabUserResourceAdmin(ImportExportModelAdmin):
#     resource_class = LabUsersResource


class LabUserAdmin(ImportExportModelAdmin):
    resource_class = LabUsersResource
    inlines = [InfoQInline, InfoAInline, PaperInline, DialogInline]
    list_display = ('user', 'nickname', 'wechat', 'group', 'classification')
    search_fields = ('user', 'nickname', 'wechat', 'group', 'classification')
    fieldsets = (
        ['Main', {
            'fields': ('user', 'nickname', 'wechat', 'group', 'classification')
        }],
    )


class PaperAdmin(admin.ModelAdmin):
    inlines = [InfoQInline]
    list_filter = ('create_time', 'finished_time', 'is_del')
    list_display = ('user', 'create_time', 'finished_time', 'is_del')
    search_fields = ('user',)
    fieldsets = (
        ['Main', {
            'fields': ('user', 'finished_time', 'is_del')
        }],
    )


class UserAttrAdmin(admin.ModelAdmin):
    inlines = [InfoQInline, AttrOptionInline]
    list_display = ('attr', 'is_option')
    list_filter = ('attr', 'is_option')
    search_fields = ('attr',)
    fieldsets = (
        ['Main', {
            'fields': ('attr', 'is_option')
        }],
    )


class UserInfoQAdmin(admin.ModelAdmin):
    inlines = [InfoAInline]
    list_display = ('user', 'paper', 'attr', 'is_del')
    list_filter = ('paper', 'attr', 'is_del')
    search_fields = ('user', 'paper', 'attr')
    fieldsets = (
        ['Main', {
            'fields': ('user', 'paper', 'attr', 'is_del')
        }],
    )


class UserInfoAAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'create_time', 'is_del')
    list_filter = ('question', 'answer', 'is_del')
    search_fields = ('user', 'question', 'answer')
    fieldsets = (
        ['Main', {
            'fields': ('user', 'question', 'answer', 'is_del')
        }],
    )


class AttrOptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'attr')
    list_filter = ('option', 'attr')
    search_fields = ('option', 'attr')
    fieldsets = (
        ['Main', {
            'fields': ('option', 'attr')
        }],
    )


class DialogAdmin(admin.ModelAdmin):
    list_display = ('user', 'recorder', 'log_time')
    list_filter = ('user', 'recorder')
    fieldsets = (
        ['Main', {
            'fields': ('user', 'recorder', 'dialog')
        }],
    )


admin.site.register(LabUser, LabUserAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(UserInfoQ, UserInfoQAdmin)
admin.site.register(UserInfoA, UserInfoAAdmin)
admin.site.register(UserAttr, UserAttrAdmin)
admin.site.register(AttrOption, AttrOptionAdmin)
admin.site.register(Dialog, DialogAdmin)
admin.site.register(LearnedCourse)
admin.site.register(LearningSchedule)
