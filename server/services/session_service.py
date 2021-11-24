import server.configs.JWT as JWT_CONFIG

sessions = []


def create_session(user_id, refresh_token, fingerprint):
    if len(sessions) == JWT_CONFIG.MAX_REFRESH_TOKENS_NUMBER:
        sessions.clear()

    sessions.append({
        'user_id': user_id,
        'refresh_token': refresh_token,
        'fingerprint': fingerprint
    })


def check_fingerprint(refresh_token, fingerprint):
    for session in sessions:
        if session['refresh_token'] == refresh_token and session['fingerprint'] == fingerprint:
            return True

    return False


def get_user_id(refresh_token):
    for session in sessions:
        if session['refresh_token'] == refresh_token:
            return session['user_id']

    return None


def remove_session(refresh_token):
    for idx in range(len(sessions)):
        if sessions[idx]['refresh_token'] == refresh_token:
            sessions.pop(idx)
            return
