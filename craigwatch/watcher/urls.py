from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'listing/(?P<id>\d+)', views.listing_page,name='listing_page'),
    url(r'settings', views.settings,name='settings'),
    url(r'preferences', views.preferences_page,name='preferences_page'),
    url(r'edit_itemhunt', views.edit_itemhunt,name='edit_itemhunt'),
    url(r'manage_itemhunts', views.manage_itemhunts, name='manage_itemhunts'),
    url(r'edit_itemhunt/process_itemhunt', views.process_itemhunt, name='process_itemhunt')
    # url(r'^register/$', core_views.signup, name='register'),
]