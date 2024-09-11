from django.utils.deprecation import MiddlewareMixin
from knox.auth import TokenAuthentication
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed
from knox.models import AuthToken
from knox.settings import CONSTANTS

class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path != '/login/' and 'HTTP_AUTHORIZATION' not in request.META:
            token = request.COOKIES.get('LOGGED_IN')
            
            if token:
                request.META['HTTP_AUTHORIZATION'] = f'Token {token}'


from django.http import HttpResponseNotFound,Http404

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_superuser:
            res=HttpResponseNotFound()
            res.delete_cookie('LOGGED_IN')
            return res
        return self.get_response(request)