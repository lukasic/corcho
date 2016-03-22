from django.template import RequestContext

from corcho import settings

def app_settings(request):
    return {
        "settings": settings,
    }

