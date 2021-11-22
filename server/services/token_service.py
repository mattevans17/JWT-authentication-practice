import uuid
from jwt import encode, decode
import server.services.session_services as session_services
import server.utils.security as security

JWT_SECRET = 'secretpassphrase'
JWT_ALGORITHM = 'HS256'


def generate_access_token(user_id):
    payload = {
        'user_id': user_id
    }

    return encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(access_token):
    return decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def generate_refresh_token():
    return str(uuid.uuid4())


def refresh_access_token(refresh_token, user_agent):
    user_id = session_services.get_user_id(refresh_token)

    if not user_id:
        return {
            'status': 'failure',
            'message': 'invalid token'
        }

    is_same_fingerprint = session_services.check_fingerprint(
        refresh_token, security.encode_user_agent(user_agent)
    )

    if not is_same_fingerprint:
        return {
            'status': 'failure',
            'message': 'invalid fingerprint'
        }

    return {
        'status': 'success',
        'access_token': generate_access_token(user_id)
    }