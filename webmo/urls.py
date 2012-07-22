from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^signup', 'main.views.signup', name='signup'),
    url(r'^login', 'main.views.login_view', name='login'),
    url(r'^logout', 'main.views.logout_view', name='logout'),
    url(r'^auth/(?P<auth_token>\w+)$', 'main.mobile.auth'),
    url(r'^auth', 'main.views.auth_view', name='auth'),
    url(r'^user/(?P<username>\w+@\w+\.\w+)/loc/(?P<loc>\d+)/status', 'main.mobile.status'),
    url(r'^user/(?P<username>\w+@\w+\.\w+)/loc/(?P<loc>\d+)/tabs', 'main.mobile.tabs'),
    url(r'^user/(?P<username>\w+@\w+\.\w+)/history', 'main.mobile.history'),

    url(r'^hq/$', 'main.views.hq', name='hq'),
    url(r'^hq/application$', 'main.views.create_application', name='create_application'),
    url(r'^hq/application/delete$', 'main.views.delete_application', name='delete_application'),

    # DEPRECATED: NOW IN ITS OWN HEROKU APP
    # url(r'^checkin/', include('checkin.urls')),
    # Examples:
    # url(r'^$', 'webmo.views.home', name='home'),
    # url(r'^webmo/', include('webmo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
