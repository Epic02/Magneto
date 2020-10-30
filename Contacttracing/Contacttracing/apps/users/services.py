import logging
import datetime
from django.db.utils import IntegrityError
from mew.core.exceptions import InvalidInputException
from .models import User
from .filters import UserFilter
from .validators import GetUserValidator
from .serializers import UserSerializer
from .constants import UserFields

logger = logging.getLogger(__name__)


class UserService():

    def get_user(self, request):
        users_data = []
        result = UserFilter(request.GET, queryset=User.objects.filter(is_deleted=False))
        serialized_data = UserSerializer(instance=result.qs, many=True).data
        if len(serialized_data) == 0:
            InvalidInputException('Data not found')
        return None, serialized_data

    def create_user(self, data):
        logger.debug(data)
        print(data)
        GetUserValidator().validate(data)
        username = data.get('username', False)
        email = data.get('email', False)
        phone = data.get('phone', False)
        aadhar_number = data.get('aadhar_number', False)
        password = data.get('password', False)
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        last_name = data.get('last_name')
        currency = data.get('currency')
        language = data.get('language')
        timezone = data.get('timezone')
        if not username or not aadhar_number or not email or not phone or not password:
            raise InvalidInputException('Username/aadhar/email/password is missing')
        try:
            obj = User.objects.get(username=username, email=email, phone=phone)
            raise InvalidInputException('User already exists')
        except User.DoesNotExist:
            obj = User.objects.create_user(username=username, password=password, email=email, phone=phone,
                                           date_of_birth=date_of_birth, gender=gender, first_name=first_name, last_name=last_name, middle_name=middle_name,
                                           currency=currency, language=language, timezone=timezone, aadhar_number=aadhar_number)
            obj.save()
        user_id = getattr(obj, 'id')
        print(user_id)
        qs = UserSerializer(instance=obj).data
        return None, qs

    def update_user(self, request, user_id):
        """"""
        data_to_update = request
        doesnt_exist = []
        try:
            user_obj = User.objects.get(id=user_id)
            for key, value in data_to_update.items():
                if key in UserFields.USER_FIELDS.value:
                    setattr(user_obj, key, value)
                else:
                    doesnt_exist.append(key)
                    data_to_update.pop(key)
            user_obj.save()
            if len(doesnt_exist):
                error = ""
                for i in doesnt_exist:
                    error = error + i + ', '
                error = 'Fields ' + error + 'do not exist.'
                raise InvalidInputException(error)
            res = data_to_update
        except User.DoesNotExist:
            raise InvalidInputException('The given id doesnt exist')
        return None, res
