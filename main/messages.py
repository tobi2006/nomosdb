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
        uniname,
        username,
        password,
        admin_email,
        admin_name
    )
    return message

