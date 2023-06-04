import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone_number(value):
    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError(_('Invalid phone number format.'))
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(_('Invalid phone number format.'))
    


