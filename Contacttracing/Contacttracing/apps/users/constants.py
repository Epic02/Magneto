import enum


class UserFields(enum.Enum):
    USER_FIELDS = ['username', 'first_name', 'middle_name', 'last_name', 'account_type', 'email',
                   'phone', 'is_staff', 'is_active', 'profile_pic', 'date_of_birth', 'gender',
                   'currency', 'language', 'timezone']


class FieldTypes(enum.Enum):
    GENDER_TYPES = ['male', 'female', 'other']
    LANGUAGES = ['english']
    CURRENCIES = ['INR']
    ACCOUNT_TYPES = ['patient', 'doctor']
    CITIES = ['bengaluru', 'chennai']
