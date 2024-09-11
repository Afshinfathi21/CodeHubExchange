from rest_framework.views import exception_handler
from django.http import HttpResponseRedirect,HttpResponseNotFound,HttpResponseServerError,Http404
from django.urls import reverse
from django.contrib.auth import logout

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    
    if response is not None:
        if response.status_code == 404 or response.status_code == 400:
            response = HttpResponseNotFound()
        elif response.status_code==401 or response.status_code==403 or response.status_code==405:
            request = context.get('request')
            next_url = request.GET.get('next')
            if next_url:
                redirect_url = f"{reverse('login')}?next={next_url}"
            else:
                redirect_url = reverse('home')
    
            response = HttpResponseRedirect(redirect_url)

            response.delete_cookie('LOGGED_IN')
            logout(request)

        elif response.status_code > 499:
            response=HttpResponseServerError()
        


    return response
