import re

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from auth.models import User
from insider.services import Serialization

serialization = Serialization()
user_model = User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        do_checking_api_key = True

        if self.is_available_path(request):
            do_checking_api_key = False

        if do_checking_api_key:
            user = user_model.objects.select_related().filter(api_key=self.get_api_key(request))

            if self.is_user_exists(user):
                request.user = user.get()
                return None
            else:
                return JsonResponse({
                    'message': 'Unauthorized'
                }, status=401)
        else:
            user = True
            return None

    def is_available_path(self, request):
        path_in_url = re.search('/home|/login|/register|/confirm|/reset', request.path)

        if path_in_url:
            return True
        return False

    def is_user_exists(self, user):
        if user:
            return True
        return False

    def get_api_key(self, request):
        if self.is_method_get(request):
            return request.GET.get('api_key')
        return serialization.json_decode(request.body)['api_key']

    def is_method_get(self, request):
        if request.method == 'GET':
            return True
        return False

    def process_response(self, request, response):
        return response