# This is essentially just a file to save longer strings, for example sample emails.
from main.unisettings import *
from main.models import Setting

def new_staff_email(name, username, password):
    uni_name = Setting.objects.get(name='uni_name').value
    nomosdb_url = Setting.objects.get(name='nomosdb_url').value
    admin_email = Setting.objects.get(name='admin_email').value
    admin_name = Setting.objects.get(name='admin_name').value
    message = """
Dear %s,

You now have access to NomosDB, the Data System for %s

The database is available at %s, and you can access
it with the following details:

Username: %s
Password: %s

When you log in, you can change your password if you click on 'My Account'.

If you experience problems, please contact %s - thanks a lot!

Enjoy the experience,

%s """ % (
        name,
        uni_name,
        nomosdb_url,
        username,
        password,
        admin_email,
        admin_name
    )
    return message


def password_reset_email(name, username, password):
    uni_name = Setting.objects.get(name='uni_name').value
    admin_name = Setting.objects.get(name='admin_name').value
    admin_email = Setting.objects.get(name='admin_email').value
    message = """
Dear %s,

You have requested your details from NomosDB, the Data System for %s. Here they
are:

Username: %s
Password: %s

Please be aware that the form is case sensitive, so make sure you use upper-
and lowercase correctly.

After successfully logging in with the above details, please click on
"My Account" and change your password to one that is both easy to remember
and difficult to guess. Make sure you do not use the same password for many
different websites. A good way to ensure password safety and convenience is
to use a password manager like KeepassX, Last Pass or One Password. All of
them are available for almost all browsers and platforms.

If you are having problems, please contact %s.

Best wishes,

%s
""" % (
        name,
        uni_name,
        username,
        password,
        admin_email,
        admin_name
    )
    return message

def attendance_email(student, modules, admin_name):
    lacking = False
    if len(modules) == 1:
        if modules[0][1].startswith('0'):
            lacking = 'did not attend any sessions in %s' % (modules[0][0])
        else:
            lacking = 'only attended %s sessions in %s' % (
                modules[0][1], modules[0][0])
    elif len(modules) == 2:
        if modules[0][1].startswith('0'):
            lacking = 'did not attend any sessions in %s' % (modules[0][0])
            none_1 = True
        else:
            lacking = 'only attended %s sessions in %s' % (
                modules[0][1], modules[0][0])
            none_1 = False
        if modules[1][1].startswith('0'):
            if none_1:
                lacking += ' and %s' % (modules[1][0])
            else:
                lacking += ' and no sessions in %s' % (modules[1][0])
    else:
        no_attendance = []
        some_attendance = []
        lacking = False
        for module in modules:
            if module[1].startswith('0'):
                no_attendance.append(module)
            else:
                some_attendance.append(module)
        if no_attendance:
            if len(no_attendance) == 1:
                lacking = 'did not attend any sessions in %s' % (
                    no_attendance[0][0])
            elif len(no_attendance) == 2:
                lacking = 'did not attend any sessions in %s and %s' % (
                    no_attendance[0][0], no_attendance[1][0])
            else:
                lacking = 'did not attend any sessions in '
                for module in no_attendance[:-1]:
                    lacking += '%s, ' % (module[0])
                lacking += 'and %s' % (no_attendance[-1][0])
        if some_attendance:
            if lacking:
                lacking += ', and you '
            else:
                lacking = ''
            if len(some_attendance) == 1:
                lacking += 'only attended %s sessions in %s' % (
                    some_attendance[0][1], some_attendance[0][0])
            elif len(some_attendance) == 2:
                lacking += 'only attended %s sessions in %s and %s sessions in %s' % (
                    some_attendance[0][1], some_attendance[0][0], some_attendance[1][1], some_attendance[1][0])
            else:
                for module in some_attendance[:-1]:
                    lacking += 'only attended %s sessions in %s, ' % (module[1], module[0])
                lacking += 'and %s sessions in %s' % (some_attendance[-1][1], some_attendance[-1][0])
    if student.tutor:
        tutor = ', ' + student.tutor.name()
    else:
        tutor = ''
    lines = ['Dear %s,' % (student.short_first_name())]
    line1 = (
        'According to our registers, you %s, and I ' +
        'would just like to find out if everything is ok and this is ' +
        'just an oversight on your part. To alleviate our worries and ' +
        'stop this escalating to a higher level, please can you contact ' +
        'me to explain your reasons for not attending as if there is ' +
        'anything we can do to help we will do our best.'
    ) % (lacking)
    lines.append(line1)
    line2 = (
        'If I do not hear from you within one week, I will escalate the ' +
        'issue to your personal tutor%s.'
    ) % (tutor)
    lines.append(line2)
    lines.append('I hope to hear from you at your earliest convenience.')
    lines.append('Many thanks and best wishes,')
    lines.append(admin_name)
    return lines
