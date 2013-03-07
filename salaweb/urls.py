from django.conf.urls import patterns, url

urlpatterns = patterns(
    'salaweb.views',
    url(r'^$', 'index', name='index'),
    url(r'^login/$', 'login_view', name='login'),
)
