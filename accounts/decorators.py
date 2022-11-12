from django.http import HttpResponse
from django.shortcuts import redirect


# using in the views for logging user and registering user
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# defining admin roles and customer roles and redirecting them
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            # checking if user is part of a group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # if admin' is in allowed_roles then return this function
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator



def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)


    return wrapper_function