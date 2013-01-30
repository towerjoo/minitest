from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('account.views',
    # Examples:
    # url(r'^$', 'minitest.views.home', name='home'),
    # url(r'^minitest/', include('minitest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/$', 'login', name='login'),
    url(r'^secret/$', 'secret', name='secret'),
    url(r'^logout/$', 'logout', name='logout'),
)
