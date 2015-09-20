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
    url(
        r'^address_nines/(\w+)/(\d{4})/$',
        'address_nines',
        name='address_nines'
    ),
    url(r'^admin_dashboard/$', 'admin', name='admin'),
    url(
        r'^all_attendances/([-\w]+)/(\w+)/$',
        'all_attendances',
        name='all_attendances'
    ),
    url(
        r'all_tutee_meetings/([-\w]+)/(\w+)/$',
        'all_tutee_meetings',
        name='all_tutee_meetings'
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
    url(r'^cause_error/', 'cause_error', name='cause_error'),
    url(
        r'^concessions/(\w+)/(\d{4})/(\w+)/$',
        'concessions',
        name='concessions'
    ),
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
    url(
        r'^edit_exam_ids/([-\w]+)/(\d{1})/$',
        'edit_exam_ids',
        name='edit_exam_ids'
    ),
    url(r'^edit_staff/(\w+)/$', 'add_or_edit_staff', name='edit_staff'),
    url(r'^edit_student/(\w+)/$', 'add_or_edit_student', name='edit_student'),
    url(
        r'^enter_student_progression/([-\w]+)/(\d{1})/$',
        'enter_student_progression',
        name='enter_student_progression'
    ),
    url(
        r'^enter_student_progression/([-\w]+)/$',
        'enter_student_progression',
        name='enter_student_progression'
    ),
    url(
        r'^tutee_meeting/(\w+)/([-\w]+)/$',
        'student_view',
        name='tutee_meeting'
    ),
    url(
        r'^tutor_list/([-\w]+)/(\d{1})/$',
        'tutor_list',
        name='tutor_list'
    ),
    url(
        r'^export_all_marks/([-\w]+)/(\d{4})/(\d{1})/$',
        'export_all_marks',
        name='export_all_marks'
    ),
    url(
        r'^export_changed_marks/([-\w]+)/(\d{4})/(\d{1})/(\d{4})/(\d+)/(\d+)/$',
        'export_changed_marks',
        name='export_changed_marks'
    ),
    url(
        r'^export_attendance_sheet/(\w+)/(\d{4})/$',
        'export_attendance_sheet',
        name='export_attendance_sheet'
    ),
    url(
        r'^export_exam_board_overview/([-\w]+)/(\d{4})/(\d{1})/$',
        'export_exam_board_overview',
        name='export_exam_board_overview'
    ),
    url(
        r'^export_resit_exam_board_overview/([-\w]+)/(\d{4})/(\d{1})/$',
        'export_resit_exam_board_overview',
        name='export_resit_exam_board_overview'
    ),
    url(
        r'^export_examiner_pack/(\w+)/(\d{4})/$',
        'export_examiner_pack',
        name='export_examiner_pack'
    ),
    url(
        r'^export_marks/(\w+)/(\d{4})/$',
        'export_marks_for_module',
        name='export_marks_for_module'
    ),
    url(
        r'^export_nors/([-\w]+)/(\d{4})/(\w+)/$',
        'export_nors',
        name='export_nors'
    ),
    url(
        r'^export_problem_students/([-\w]+)/(\d{4})/(\w+)/$',
        'export_problem_students',
        name='export_problem_students'
    ),
    url(
        r'^export_problem_students_after_resits/([-\w]+)/(\d{4})/(\w+)/$',
        'export_problem_students_after_resits',
        name='export_problem_students_after_resits'
    ),
    url(
        r'^export_tier_4_attendance/([-\w]+)/(\d{4})/$',
        'export_tier_4_attendance',
        name='export_tier_4_attendance'
    ),
    url(
        r'^invite_students/([-\w]+)/$',
        'invite_students',
        name='invite_students'
    ),
    url(r'^main_settings/$', 'main_settings', name='main_settings'),
    url(
        r'^mark_all/([-\w]+)/(\d{4})/([-\w]+)/(\w+)/',
        'mark_all',
        name='mark_all'
    ),
    url(
        r'^mark_all_anonymously/([-\w]+)/(\d{4})/([-\w]+)/(\w+)/',
        'mark_all_anonymously',
        name='mark_all_anonymously'
    ),
    url(r'^my_tutees/$', 'my_tutees', name='my_tutees'),
    url(r'^module/(\w+)/(\d{4})/$', 'module_view', name='module_view'),
    url(r'^parse_csv/(\w+)/$', 'parse_csv', name='parse_csv'),
    url(
        r'^remove_student_from_module/(\w+)/(\d{4})/(\w+)/$',
        'remove_student_from_module',
        name='remove_student_from_module'
    ),
    url(
        r'^proceed_to_next_year/$',
        'proceed_to_next_year',
        name='proceed_to_next_year'
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
    url(
        r'^toggle_assessment_availability/(\w+)/(\d{4})/([-\w]+)/(\w+)/$',
        'toggle_assessment_availability',
        name='toggle_assessment_availability'
    ),
    url(r'^upload_exam_ids/$', 'upload_exam_ids', name='upload_exam_ids'),
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

urlpatterns += patterns(
    'feedback.views',
    url(
        r'^group_feedback/(\w+)/(\d{4})/([-\w]+)/(\w+)/$',
        'group_feedback',
        name='group_feedback_first_attempt'
    ),
    url(
        r'^group_feedback/(\w+)/(\d{4})/([-\w]+)/(\w+)/(\w+)/$',
        'group_feedback',
        name='group_feedback'
    ),
    url(
        r'^export_feedback/(\w+)/(\d{4})/([-\w]+)/(\w+)/(\w+)/$',
        'export_feedback',
        name='export_feedback'
    ),
    url(
        r'^individual_feedback/(\w+)/(\d{4})/([-\w]+)/(\w+)/$',
        'individual_feedback',
        name='individual_feedback_first_attempt'
    ),
    url(
        r'^individual_feedback/(\w+)/(\d{4})/([-\w]+)/(\w+)/(\w+)/$',
        'individual_feedback',
        name='individual_feedback'
    ),
)
