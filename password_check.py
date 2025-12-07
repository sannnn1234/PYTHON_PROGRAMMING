import re

def check_password_strength(password):
    # Check minimum length
    if len(password) < 8:
        return False

    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # Check for lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # Check for at least one digit
    if not re.search(r"[0-9]", password):
        return False

    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


password = input("Enter a password to check its strength: ")

if check_password_strength(password):
    print("Strong Password")
else:
    print("Weak Password! Make sure it:")
    print("Has at least 8 characters")
    print("Contains both UPPERCASE and lowercase letters")
    print("Contains at least one digit (0-9)")
    print("Contains at least one special character (!@#$ etc.)")