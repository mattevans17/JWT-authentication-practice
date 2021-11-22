import server.services.token_service as token_service
import server.utils.security as security
import server.services.session_services as session_services
import server.services.account_service as data_api


def authorization(user_id, user_agent):
    # Делаем fingerprint из UA (вместо библиотеки)
    fingerprint = security.encode_user_agent(user_agent)

    refresh_token = token_service.generate_refresh_token()

    # Создание сессии и запись refresh токена
    session_services.create_session(user_id, refresh_token, fingerprint)

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
