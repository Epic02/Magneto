import django_filters as df
from django.contrib.auth.models import User


class UserFilter(df.FilterSet):

    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            # 'username': ['exact'],
            # 'first_name': ['exact', 'icontains'],
            # 'middle_name': ['exact', 'icontains'],
            # 'last_name': ['exact', 'icontains'],
            # 'account_type': ['exact'],
            # 'aadhar_number': ['exact'],
            # 'email': ['exact'],
            # 'phone': ['exact'],
            # 'is_staff': ['exact'],
            # 'is_active': ['exact'],
            # 'date_of_birth': ['exact', 'icontains'],
            # 'gender': ['exact'],
            # 'currency': ['exact'],
            # 'language': ['exact'],
            # 'timezone': ['exact'],
        }
