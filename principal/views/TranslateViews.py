from django.http.response import HttpResponseRedirect
from django.utils import translation

def change_language(request):
    user_language = request.GET['language']
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
