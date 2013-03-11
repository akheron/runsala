from django.conf.urls import patterns, url

urlpatterns = patterns(
    'salaweb.views',
    url(r'^$', 'index', name='index'),
    url(r'admin/$', 'admin', name='admin'),
    url(r'ajax/(?P<repository>[^/]+)/(?P<path>.*)$', 'ajax', name='ajax'),
    url(r'settings/$', 'settings', name='settings'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)
