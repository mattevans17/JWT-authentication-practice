import uuid
from run import app
from jwt import encode, decode
import server.services.session_service as session_service
from server.utils import crypto, date_time
import server.configs.JWT as JWT_CONFIG


def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': date_time.calc_exp(JWT_CONFIG.ACCESS_TOKEN_EXP_SEC)
    }

    return encode(payload, app.config['SECRET_KEY'], algorithm=JWT_CONFIG.ALGORITHM)


def decode_access_token(access_token):
    return decode(access_token, app.config['SECRET_KEY'], algorithms=[JWT_CONFIG.ALGORITHM])


def generate_refresh_token():
    return str(uuid.uuid4())


def refresh_tokens(refresh_token, user_agent):
    invalid_token_error = {
        'status': 'failure',
        'message': 'invalid token'
    }

    if not refresh_token:
        return invalid_token_error

    session = session_service.get_session(refresh_token)

    if not session:
        session_service.remove_session(refresh_token)
        return invalid_token_error

    is_expired = date_time.check_expired(session['expires_in'])
    if is_expired:
        session_service.remove_session(refresh_token)
        return invalid_token_error

    is_same_fingerprint = session_service.check_fingerprint(
        refresh_token, crypto.encode_user_agent(user_agent)
    )

    if not is_same_fingerprint:
        session_service.remove_session(refresh_token)
        return invalid_token_error

    new_refresh_token = generate_refresh_token()
    session_service.create_session(
        session['user_id'],
        new_refresh_token,
        crypto.encode_user_agent(user_agent)
    )
    session_service.remove_session(refresh_token)

    return {
        'status': 'success',
        'refresh_token': new_refresh_token,
        'access_token': generate_access_token(session['user_id'])
    }
