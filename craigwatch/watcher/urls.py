from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'listings/(?P<id>\d+)', views.listing_page,name='listing_page'),
    url(r'settings', views.settings,name='settings')
]