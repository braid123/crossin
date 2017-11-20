from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.student_group, name='group'),
    url(r'^student', views.student_group, name='studentgroup'),
]
