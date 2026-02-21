import re

RAW_PRIVACY_CATEGORIES = {
    "email", 
    "username", 
    "user_id", 
    "ip_address",
    "device_id",
    "auth_token",
    "session_id",
    "password", 
    "phonenumber",
    "credit_card",
    "social_security_number",
    "biometric_data",
    "health_data",
    "financial_data",
    "personal_identifier",
    "contact_info",
    "demographic_info",
    "behavioral_data",
    "location_data",
    "communication_data",
    "jwt_token",
    "oauth_token",
    "api_key",
    "cookie", 
    "geo_location",
    "mac_address",
}

def normalize_key(key: str) -> str:
    return re.sub(r'[^a-z0-9]', '', key.lower())

PRIVACY_CATEGORIES = {
    normalize_key(cat) for cat in RAW_PRIVACY_CATEGORIES
}
