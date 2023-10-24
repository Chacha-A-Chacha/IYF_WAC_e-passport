import string
import secrets


def generate_temp_password(length=12):
    """
    Generate a temporary password with the specified length.

    Parameters:
    - length (int): Length of the generated password. Default is 12 characters.

    Returns:
    - str: Generated temporary password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    temp_password = ''.join(secrets.choice(characters) for _ in range(length))
    return temp_password

# Example usage
# temp_password = generate_temp_password()
# print(temp_password)
