from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'database.views',
    url(r'^$', 'home', name='home'),
    url(r'^add_student/$', 'add_or_edit_student', name='add_student'),
    url(r'^student/(\w+)/$', 'student_view', name='student_view'),
    url(r'^edit_student/(\w+)/$', 'add_or_edit_student', name='edit_student'),
)
