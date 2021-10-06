from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url(r'^profiles$', views.profiles),
    url(r'^profiles/(?P<id>[0-9]+)$', views.profile),
    url(r'^profiles/(?P<id>[0-9]+)/edit$', views.profile_edit)
]