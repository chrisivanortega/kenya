
from django.http import HttpResponse,HttpResponseRedirect


def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        try:
            admin = request.session['name']['username']
        except:
            admin = False
        if admin == 'admin':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap