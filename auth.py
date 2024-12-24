import secrets
import string

def generate_token(data: dict):
    length = 32
    alphabet = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string
