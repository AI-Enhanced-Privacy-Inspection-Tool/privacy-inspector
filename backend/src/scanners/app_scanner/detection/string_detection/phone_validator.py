import re
import phonenumbers
from phonenumbers import NumberParseException

NON_PHONE_NUMBER_PATTERNS = {
    '://', # URLs
    '.jar', '.py', '.js', '.ts', '.txt', # file paths
}

def is_valid_phone_number(phone_number, region=None, min_digits=7):
    """
    Returns True if `phone_number` is a valid phone number and False otherwise.

    - Requires at least `min_digits` numeric digits before attempting to parse
    - `region` is the default region (e.g., "FI").
    - Doesn't accept anything with letters
    """

    if not phone_number or not isinstance(phone_number, str):
        return False
    
    # if its too long, it's unlikely to be a phone number
    if len(phone_number) > 25:
        return False

    # reject if contains letters
    if re.search(r"[A-Za-z]", phone_number):
        return False

    # count digits only
    digits_only = re.sub(r"\D", "", phone_number)
    if len(digits_only) < min_digits:
        return False
    
    # if it contains periods, shashes or colons, it's unlikely to be a phone number
    if re.search(r"[.:]", phone_number):
        return False

    # if it contains patterns that are unlikely for phone numbers, reject
    for pattern in NON_PHONE_NUMBER_PATTERNS:
        if pattern in phone_number:
            return False

    # if the number includes an international prefix, parse without a default region first
    if phone_number.startswith('+'):
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                return True
        except NumberParseException:
            pass

    # if a region was provided, try parsing with it
    if region:
        try:
            parsed_number = phonenumbers.parse(phone_number, region)
            if phonenumbers.is_valid_number(parsed_number):
                return True
        except NumberParseException:
            pass

    return False
    
# test functionality with some example phone numbers
if __name__ == "__main__":
    test_numbers = [
        # should return True
        "+1 650-253-0000",  # valid US number
        "020 7031 3000",    # valid UK number
        "+358 9 1234567",   # valid Finnish number
        "+49 30 12345678", # valid German number
        "+81 3-1234-5678", # valid Japanese number

        # good to return True, but okay if they return False since they are borderline cases
        "+1 800 FLOWERS",   # valid US vanity number
        "Call me at 555-12345", # contains a valid number but also text
        "+86 10 1234 5678 For my work phone", # valid Chinese number with text

        # should return False
        "12345",            # too short
        "98732459873459873459873645983746537645893746583745", # too long
        "abcde",            # letters only
        "not a phone number", # not a phone number
        None,               # None input
        "Downloaded full file for project Farsight [Forge/Neo] - (495693) in 234ms", # not a phone number but contains digits
        "utw6159vm705o", # not a phone number but contains digits
        "https://libraries.numnum.net/net/java/dev/jna/jna/5.17.0/jna-5.17.0.jar", # not a phone number but contains digits
        "net/java/dev/jna/jna/5.17.0/jna-5.17.0.jar", # not a phone number but contains digits
        "1.258.0.17869", # not a phone number
        "s876987f6s87686787967876976fds897987g87fg876g876g", # not a phone number but contains digits
        "987DSFG98D7FG98D7FG987DFGD98GF7D9G8F7",
        "log4j2-xml",
        "1.8.1-pre5",
        "HPCUST1.exe",
        "Hx6Q.tsx",
        "7200000",
        "1534956090",
        "1709994102048",
        "Virheellinen puhelinnumero",
        "2015-10-12", 
        "12/10/2015", 
        "10.12.2015", 
        "2011-08-26T19:44:00Z",
    ]

    for number in test_numbers:
        print(f"{number}: {is_valid_phone_number(number)}")