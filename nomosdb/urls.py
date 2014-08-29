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
    url(r'^add_course/$', 'add_or_edit_course', name='add_course'),
    url(r'^add_module/$', 'add_or_edit_module', name='add_module'),
    url(r'^add_staff/$', 'add_or_edit_staff', name='add_staff'),
    url(r'^add_student/$', 'add_or_edit_student', name='add_student'),
    url(
        r'^add_students_to_module/(\w+)/(\d{4})/$', 
        'add_students_to_module',
        name='add_students_to_module'
    ),
    url(r'^admin_dashboard/$', 'admin', name='admin'),
    url(r'^assessment/(\w+)/(\d{4})/$', 'assessment', name='assessment'),
    url(
        r'^assign_seminar_groups/(\w+)/(\d{4})/$',
        'assign_seminar_groups',
        name='assign_seminar_groups'
    ),
    url(r'^attendance/(\w+)/(\d{4})/(\w+)/$', 'attendance', name='attendance'),
    url(r'^course_overview/$', 'course_overview', name='course_overview'),
    url(
        r'^delete_assessment/(\w+)/(\d{4})/([-\w]+)/$',
        'delete_assessment',
        name='delete_assessment'
    ),
    url(
        r'^edit_assessment/(\w+)/(\d{4})/([-\w]+)/$',
        'assessment',
        name='edit_assessment'
    ),
    url(r'^edit_course/(\d+)/$', 'add_or_edit_course', name='edit_course'),
    url(
        r'^edit_module/(\w+)/(\d{4})/$',
        'add_or_edit_module',
        name='edit_module'
    ),
    url(r'^edit_staff/(\w+)/$', 'add_or_edit_staff', name='edit_staff'),
    url(r'^edit_student/(\w+)/$', 'add_or_edit_student', name='edit_student'),
    url(r'^module/(\w+)/(\d{4})/$', 'module_view', name='module_view'),
    url(
        r'^remove_student_from_module/(\w+)/(\d{4})/(\w+)/$',
        'remove_student_from_module',
        name='remove_student_from_module'
    ),
    url(
        r'^seminar_group_overview/(\w+)/(\d{4})/$',
        'seminar_group_overview',
        name='seminar_group_overview'
    ),
    url(r'^student/(\w+)/$', 'student_view', name='student_view'),
    url(r'^subject_areas/$', 'subject_areas', name='subject_areas'),
    url(
        r'^view_staff_by_name/$',
        'view_staff_by_name',
        name='view_staff_by_name'
    ),
    url(
        r'^view_staff_by_subject/$',
        'view_staff_by_subject',
        name='view_staff_by_subject'
    ),
)
