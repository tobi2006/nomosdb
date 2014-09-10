# This is essentially just a file to save longer strings, for example sample emails.
from main.unisettings import *
from main.models import Settings

def new_staff_email(name, username, password):
    uni_name = Settings.objects.get(name='uni_name').value
    nomosdb_url = Settings.objects.get(name='nomosdb_url').value
    admin_email = Settings.objects.get(name='admin_email').value
    admin_name = Settings.objects.get(name='admin_name').value
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
