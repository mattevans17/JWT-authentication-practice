import uuid
from jwt import encode, decode
import server.services.session_service as session_service
import server.utils.crypto as crypto
import server.utils.date_time as date_time
import server.configs.JWT as JWT_CONFIG


def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': date_time.calc_exp(JWT_CONFIG.ACCESS_TOKEN_EXP_SEC)
    }

    return encode(payload, JWT_CONFIG.SECRET, algorithm=JWT_CONFIG.ALGORITHM)


def decode_access_token(access_token):
    return decode(access_token, JWT_CONFIG.SECRET, algorithms=[JWT_CONFIG.ALGORITHM])


def generate_refresh_token():
    return str(uuid.uuid4())


def refresh_access_token(refresh_token, user_agent):
    user_id = session_service.get_user_id(refresh_token)

    if not user_id:
        return {
            'status': 'failure',
            'message': 'invalid token'
        }

    is_same_fingerprint = session_service.check_fingerprint(
        refresh_token, crypto.encode_user_agent(user_agent)
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
