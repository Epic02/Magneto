import pytz
from mew.core.validators import RequestValidator
from mew.core.exceptions import InvalidInputException
from .constants import FieldTypes


class GetUserValidator(RequestValidator):
    schema = {
        "type": "object",
        "properties": {
            "first_name": {
                "type": "string"
            },
            "middle_name": {
                "type": "string"
            },
            "last_name": {
                "type": "string"
            },
            "email": {
                "type": "string",
            },
            "phone": {
                "type": "string",
                "pattern": "^\d{10}$",
            },
            "date_of_birth": {
                "type": "string",
                "pattern": "^(\d{4})\-(0[1-9]|1[0-2])\-([0-2][1-9]|3[0-1])$"
            },
            "password": {
                "type": "string"
            },
            "aadhar_number": {
                "type": "string",
                "pattern": "^\d{12}$",
            },
            "gender": {
                "type": "string",
                "enum": FieldTypes.GENDER_TYPES.value
            },
            "currency": {
                "type": "string",
                'enum': FieldTypes.CURRENCIES.value
            },
            "language": {
                "type": "string",
                'enum': FieldTypes.LANGUAGES.value
            },
            "timezone": {
                "type": "string"
            },
            "required": ["phone", "password", "email"]
        }
    }

    def validate(self, data):
        if not data['timezone'] in pytz.all_timezones:
            raise InvalidInputException('Timezone does not exist')
        super().validate(data)
