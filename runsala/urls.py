from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'runsala.views',
    url(r'^$', 'index', name='index'),
    url(r'admin/$', 'admin', name='admin'),
    url(r'settings/$', 'settings', name='settings'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'ajax/', include('runsala.ajax_urls')),
)
