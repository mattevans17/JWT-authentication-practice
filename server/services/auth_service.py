from server.services import session_service, account_service, token_service
from server.utils import crypto


def authorization(user_id, user_agent):
    fingerprint = crypto.encode_user_agent(user_agent)
    refresh_token = token_service.generate_refresh_token()
    session_service.create_session(user_id, refresh_token, fingerprint)
    access_token = token_service.generate_access_token(user_id)

    return access_token, refresh_token


def authentication(login, password):
    for account in account_service.accounts:
        if account['login'] == login and account['password'] == password:
            return {
                'status': 'success',
                'user_id': account['user_id']
            }

    return {
        'status': 'failure'
    }
