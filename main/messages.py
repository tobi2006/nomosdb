# This is essentially just a file to save longer strings, for example sample emails.
from nomosdb.unisettings import *

def new_staff_email(name, username, password):
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
        UNI_NAME,
        NOMOSDB_URL,
        username,
        password,
        ADMIN_EMAIL,
        ADMIN_NAME
    )
    return message
