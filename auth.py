import jwt

SECRET_KEY = "clairo"
ALGORITHM = "HS256"


def generate_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
