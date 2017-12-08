from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^search', include('haystack.urls')),
    url(r'^save', ItemSave.as_view(), name='save'),
    url(r'^questions/(\d+)/$', questions, name='questions'),
    url(r'^ask', ask, name='ask'),
    url(r'^k2qa', KeyToItem.as_view(), name='k2qa'),
]
