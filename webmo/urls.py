from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^signup/', 'main.views.signup', name='signup'),
    url(r'^login/', 'main.views.login_view', name='login'),
    url(r'^logout/', 'main.views.logout_view', name='logout'),
    url(r'^user/(?P<userid>\d+)/loc/(?P<loc>\d+)', 'main.input.android', name='android'),

    url(r'^hq/', 'main.views.hq', name='hq'),
    # Examples:
    # url(r'^$', 'webmo.views.home', name='home'),
    # url(r'^webmo/', include('webmo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
