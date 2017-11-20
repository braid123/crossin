from django.conf.urls import url, include
from . import views

ajax_patterns = [
    url(r'^modify', views.ajax_conf_modify, name='modify'),
]

urlpatterns = [
    url(r'^ajax/', include(ajax_patterns, namespace='ajax')),
    url(r'^rule', views.rule_conf, name='rule'),
    url(r'^qas', views.qa_conf_strict, name='qas'),
    url(r'^qa', views.qa_conf, name='qa'),
    url(r'^pic', views.pic_subject, name='pic'),
]
