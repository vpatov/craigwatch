from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'listing/(?P<id>\d+)', views.listing_page,name='listing_page'),
    url(r'settings', views.settings,name='settings'),
    url(r'preferences', views.preferences_page,name='preferences_page'),
    url(r'add_itemhunt', views.add_itemhunt,name='add_itemhunt')
    # url(r'^register/$', core_views.signup, name='register'),
]