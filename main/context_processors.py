from nomosdb.unisettings import *

def constants(request):
    return {
        'UNI_NAME': UNI_NAME,
        'UNI_SHORT_NAME': UNI_SHORT_NAME,
    }
