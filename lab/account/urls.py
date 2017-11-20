from django.conf.urls import url, include
from .views import register, log_in, log_out

urlpatterns = [
    url(r'^register', register, name='register'),
    url(r'^login', log_in, name='login'),
    url(r'^logout', log_out, name='logout')
]
