from django.contrib import admin
from .models import *
# Register your models here.


class RuleAddFriendInline(admin.TabularInline):
    model = RuleAddFriend


class ChatRoomAdmin(admin.ModelAdmin):
    inlines = [RuleAddFriendInline]
    list_display = ('nickname', 'order')
    search_fields = ('nickname', 'order')
    fields = ('nickname', 'order')


class RuleAddFriendAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'chatroom')
    search_fields = ('keyword', 'chatroom')
    list_filter = ('keyword', 'chatroom')
    fields = ('keyword', 'chatroom')


class QAKeyWordAdmin(admin.ModelAdmin):
    list_display = ('keyword',)
    search_fields = ('keyword',)
    fields = ('keyword',)


class QAReplyAdmin(admin.ModelAdmin):
    list_display = ('desc', 'is_pic')
    search_fields = ('desc',)
    list_filter = ('is_pic',)
    fields = ('desc', 'is_pic', 'reply_text', 'reply_pic', 'keywords')

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(RuleAddFriend, RuleAddFriendAdmin)
admin.site.register(QAKeyWord, QAKeyWordAdmin)
admin.site.register(QAReply, QAReplyAdmin)
