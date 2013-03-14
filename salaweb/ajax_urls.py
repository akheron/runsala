from django.conf.urls import patterns, url

urlpatterns = patterns(
    'salaweb.ajax_views',
    url(r'(?P<repository>[^/]+)/(?P<path>.*)$', 'secret', name='secret'),
)
