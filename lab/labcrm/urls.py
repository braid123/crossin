from django.conf.urls import url, include
from labcrm import views


ajax_urls = [
    url(r'^preview', views.ajax_conf_preview, name='preview'),
    # url(r'^modify', views.ajax_detail_modify, name='modify'),
    url(r'^add', views.ajax_conf_add, name='add'),
    url(r'^del', views.ajax_user_del, name='del'),
    url(r'^new', views.ajax_new_user, name='new')
]

modify_urls = [
    url(r'^schedule', views.modify_schedule, name='schedule')
]


urlpatterns = [
    url(r'^ajax/', include(ajax_urls, namespace='ajax')),
    url(r'^modify/', include(modify_urls, namespace='modify')),
    url(r'^users', views.user_list, name='list'),
    url(r'^detail/(?P<new_id>.*)$', views.user_detail, name='detail2'),
    url(r'^detail', views.user_detail, name='detail'),
    url(r'^papers', views.papers_create, name='papers'),
    url(r'^paper/(?P<data_key>\d*)$', views.paper_display, name='paper2'),
    url(r'^paper', views.paper_display, name='paper'),
    url(r'^conf', views.ques_conf, name='conf'),
    url(r'^fill/(?P<data_key>\d*)$', views.ques_fill, name='fill'),
    url(r'^fill', views.ques_fill, name='fill2'),
    url(r'^class', views.link_to_class, name='class'),
    url(r'^courses', views.learning_courses, name='courses'),
    url(r'^statistic', views.subject_statistic, name='statistic'),
    url(r'^schedule', views.schedule_statistic, name='schedule'),
]
