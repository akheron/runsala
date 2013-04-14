from django.conf.urls import patterns, url

urlpatterns = patterns(
    'runsala.ajax_views',
    url(r'^$', 'repository_create', name='repository_create'),
    url(r'(?P<repository>[\w-]+)/(?P<path>.*)$', 'secret', name='secret'),
)
