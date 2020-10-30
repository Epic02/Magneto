import json

from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from mew.core.utils import APIResponse
from mew.core.exceptions import InvalidInputException
from oauth2_provider.views import ProtectedResourceView
from .services import UserService


# Create your views here.


class UserView(APIView):
    def get(self, request):
        """
        :param request:
        :return:
        """
        error, res = UserService().get_user(request)
        return APIResponse.send(data=res, error=error)

    def post(self, request):
        """"""
        data = {
            'username': request.data.get('phone', None),
            'password': request.data.get('password', None),
            'first_name': request.data.get('first_name', None),
            'middle_name': request.data.get('middle_name', None),
            'last_name': request.data.get('last_name', None),
            'email': request.data.get('email', None),
            'phone': request.data.get('phone', None),
            'date_of_birth': request.data.get('date_of_birth', None),
            'gender': request.data.get('gender', None),
            'currency': request.data.get('currency', None),
            'language': request.data.get('language', None),
            'timezone': request.data.get('timezone', None),
            'aadhar_number': request.data.get('aadhar_number', None)
        }
        error, res = UserService().create_user(data)
        return APIResponse.send(data=res, error=error)

    def put(self, request, user_id):

        error, res = UserService().update_user(request.data, user_id=user_id)
        return APIResponse.send(data=res, error=error)

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'PUT':
            permission_classes = (IsAuthenticated,)
            print('GET/PUT')
        else:
            print('POST')
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]
