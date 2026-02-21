from email_validator import validate_email, EmailNotValidError

NON_EMAIL_PATTERNS = {
    '://', # URLs
    '.jar', '.py', '.js', '.ts', '.txt', '.xml', '.vast', '.http', '.http-image' 
}

def is_valid_email(email):
    """
    Validates if the input string is a valid email address.
    - Uses a simple regex pattern to check for basic email structure.
    - Ensures there are no spaces and that it contains an "@" symbol and a domain.
    """

    if len(email) > 70:
        return False
    
    # reject obviously malformed strings early
    if " " in email or email.count("@") != 1:
        return False

    # reject non-email patterns
    for pattern in NON_EMAIL_PATTERNS:
        if pattern in email:
            return False
    
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False
    except Exception:
        return False


# test functionality with some example email addresses
if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "invalid.email",
        "user@.com",
        "user@domain",
        "user@domain.c",
        "t112@2-223.3",
        "user",
        "user@user.c@user.as",
        "user@user.c   @user.as  nna",
        "emily@gmail.com ",
        "emily @gmail.com",
        "preloads#content@logic.plugin.libs.xml",
        "preloads#content@logic.transform.http-image"
    ]

    for email in test_emails:
        print(f"{email}: {is_valid_email(email)}")