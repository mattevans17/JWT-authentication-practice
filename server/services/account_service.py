import uuid


accounts = []


def create_account(login, password):
    user_id = str(uuid.uuid4())

    new_account = {
        'user_id': user_id,
        'login': login,
        'password': password
    }
    print('CREATE ACCOUNT')
    print(new_account)

    accounts.append(new_account)

    return user_id
