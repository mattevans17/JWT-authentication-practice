import uuid


accounts = [
    {
        'user_id': '123',
        'login': 'admin',
        'password': 'admin'
    }
]


def create_account(login, password):
    user_id = str(uuid.uuid4())

    new_account = {
        'user_id': user_id,
        'login': login,
        'password': password
    }

    accounts.append(new_account)

    return user_id
