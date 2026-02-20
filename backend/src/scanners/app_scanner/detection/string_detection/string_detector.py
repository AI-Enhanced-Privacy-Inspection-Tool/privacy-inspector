from .phone_validator import is_valid_phone_number
from .email_address_validator import is_valid_email  

# TODO: add more detectors here (JWT, UUID, IP, API keys, etc.)
DETECTORS = [
    ("phonenumber", "phone_validator", is_valid_phone_number),
    ("email", "email_validator", is_valid_email),
]

def detect_string_type(value: str):
    """
    Detect if the given string matches a known privacy-sensitive type.
    Each match is a dict like:
        {
            "category": str,
            "detection_method": str,
            "confidence": str
        }
    """

    for category, method, validator in DETECTORS:
        if validator(value):
            return {
                "category": category,
                "detection_method": method,
                "confidence": "high"
            }
        
    return {}
    