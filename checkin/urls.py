from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^update/(?P<username>\w+@\w+\.\w+)$', 'checkin.views.update'),
    url(r'^check/(?P<username>\w+@\w+\.\w+)$', 'checkin.views.check'),
    url(r'^register/(?P<username>\w+@\w+\.\w+)$', 'checkin.views.register'),
    url(r'^callback$', 'checkin.views.callback', name='checkin_callback'),
    # Examples:
    # url(r'^$', 'webmo.views.home', name='home'),
    # url(r'^webmo/', include('webmo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
