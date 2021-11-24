import server.services.token_service as token_service
import server.utils.crypto as crypto
import server.services.session_service as session_service
import server.services.account_service as data_api


def authorization(user_id, user_agent):
    fingerprint = crypto.encode_user_agent(user_agent)
    refresh_token = token_service.generate_refresh_token()
    session_service.create_session(user_id, refresh_token, fingerprint)
    access_token = token_service.generate_access_token(user_id)

    return access_token, refresh_token


def authentication(login, password):
    for account in data_api.accounts:
        if account['login'] == login and account['password'] == password:
            return {
                'status': 'success',
                'user_id': account['user_id']
            }

    return {
        'status': 'failure'
    }
