from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.student_group, name='studentgroup'),
    url(r'^student', views.student_group, name='studentgroup'),
]
