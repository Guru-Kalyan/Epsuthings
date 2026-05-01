import base64
import hashlib
import pytz
from django.conf import settings
from django.core.exceptions import ValidationError

get_timezone = lambda: pytz.timezone(settings.TIME_ZONE)

def get_base64_str(value: str) -> str:
    return base64.b64encode(value.encode()).decode()

def get_base64_decoded_str(value: str) -> str:
    return base64.b64decode(value.encode()).decode()

def base64ofsha(input: str) -> str:
    s = hashlib.sha256(input.encode('utf-8')).digest()
    return base64.b64encode(s).decode()

def email_validator(email: str):
    import re
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        raise ValidationError('Enter a valid email address.')

def generate_authentication_header(username, password):
    pw_b64 = get_base64_str(password)
    token_str = f"{username}:{pw_b64}"
    token = get_base64_str(token_str)
    return f"Authenticate {token}"
