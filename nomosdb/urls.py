from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'main.views',
    url(r'^$', 'home', name='home'),
    url(r'^add_module/$', 'add_or_edit_module', name='add_module'),
    url(r'^add_student/$', 'add_or_edit_student', name='add_student'),
    url(
        r'^edit_module/(\w+)/(\d{4})/$',
        'add_or_edit_module',
        name='edit_module'
    ),
    url(r'^edit_student/(\w+)/$', 'add_or_edit_student', name='edit_student'),
    url(r'^module/(\w+)/(\d{4})/$', 'module_view', name='module_view'),
    url(r'^student/(\w+)/$', 'student_view', name='student_view'),
)
