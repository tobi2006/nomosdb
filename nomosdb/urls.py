from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'database.views.home', name='home'),
    url(r'^add_student/$', 'database.views.add_student', name='add_student'),
    url(r'^admin/', include(admin.site.urls)),
)
