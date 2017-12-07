from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    # url(r'^save', item_save, name='save'),
    url(r'^save', ItemSave.as_view(), name='save'),
    # url(r'^k2qa', key_to_item, name='k2qa'),
    url(r'^k2qa', KeyToItem.as_view(), name='k2qa'),
    url(r'^ttt', MyClassView.as_view()),
]
