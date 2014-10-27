from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^admin/', include(admin.site.urls)),
    url(
        r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'
    ),
    url(
        r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'},
        name='logout'
    ),
    url(
        r'^accounts/change_password/$',
        'django.contrib.auth.views.password_change',
        {'template_name': 'password_change.html'},
        name='password_change'
    ),
    url(
        r'^accounts/change_password_done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'password_change_done.html'},
        name='password_change_done'
    ),
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
    url(
        r'^all_attendances/([-\w]+)/(\w+)/$',
        'all_attendances',
        name='all_attendances'
    ),
    url(r'^assessment/(\w+)/(\d{4})/$', 'assessment', name='assessment'),
    url(
        r'^assessment_groups/(\w+)/(\d{4})/([-\w]+)/(\w+)/$',
        'assign_assessment_groups',
        name='assessment_groups'
    ),
    url(
        r'^assessment_group_overview/(\w+)/(\d{4})/([-\w]+)/(\w+)/$',
        'assessment_group_overview',
        name='assessment_group_overview'
    ),
    url(
        r'^assign_seminar_groups/(\w+)/(\d{4})/$',
        'assign_seminar_groups',
        name='assign_seminar_groups'
    ),
    url(
        r'^assign_seminar_groups_old_browser/(\w+)/(\d{4})/$',
        'assign_seminar_groups_old_browser',
        name='assign_seminar_groups_old_browser'
    ),
    url(
        r'^assign_tutors/([-\w]+)/(\w+)/$',
        'assign_tutors',
        name='assign_tutors'
    ),
    url(r'^attendance/(\w+)/(\d{4})/(\w+)/$', 'attendance', name='attendance'),
    url(r'^course_overview/$', 'course_overview', name='course_overview'),
    url(
        r'^delete_assessment/(\w+)/(\d{4})/([-\w]+)/$',
        'delete_assessment',
        name='delete_assessment'
    ),
    url(
        r'^delete_meeting/(\w+)/$',
        'delete_tutee_meeting',
        name='delete_tutee_meeting'
    ),
    url(
        r'^delete_module/(\w+)/(\d{4})/$',
        'delete_module',
        name='delete_module'
    ),
    url(
        r'^delete_staff_member/(\w+)/$',
        'delete_staff_member',
        name='delete_staff_member'
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
    url(
        r'^edit_tutee_meeting/(\w+)/(\w+)/$',
        'student_view',
        name='edit_tutee_meeting'
    ),
    url(
        r'^export_attendance_sheet/(\w+)/(\d{4})/$',
        'export_attendance_sheet',
        name='export_attendance_sheet'
    ),
    url(r'^main_settings/$', 'main_settings', name='main_settings'),
    url(r'^my_tutees/$', 'my_tutees', name='my_tutees'),
    url(r'^module/(\w+)/(\d{4})/$', 'module_view', name='module_view'),
    url(r'^parse_csv/(\w+)/$', 'parse_csv', name='parse_csv'),
    url(
        r'^remove_student_from_module/(\w+)/(\d{4})/(\w+)/$',
        'remove_student_from_module',
        name='remove_student_from_module'
    ),
    url(r'^reset_password/$', 'reset_password', name='reset_password'),
    url(
        r'^seminar_group_overview/(\w+)/(\d{4})/$',
        'seminar_group_overview',
        name='seminar_group_overview'
    ),
    url(r'^search_student/$', 'search_student', name='search_student'),
    url(r'^student/(\w+)/$', 'student_view', name='student_view'),
    url(r'^students/(\w+)/$', 'year_view', name='year_view'),
    url(r'^subject_areas/$', 'subject_areas', name='subject_areas'),
    url(r'^upload_csv_file/$', 'upload_csv', name='upload_csv'),
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
    url(r'^wrong_email/$', 'wrong_email', name='wrong_email'),
)
