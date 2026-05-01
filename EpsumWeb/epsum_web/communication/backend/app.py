from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator

def validate_email_address(value):
    try:
        validate_email(value)
    except Exception:
        raise ValidationError("Enter a valid email address")


mobile_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Enter a valid mobile number"
)

