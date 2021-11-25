user_data = [{
    'user_id': '123',
    'data': {
        'cars': [
            {
                'brand': 'Koenigsegg',
                'model': 'Regera'
            }
        ]
    }
}]


def get_data(user_id):
    for idx in range(len(user_data)):
        if user_data[idx]['user_id'] == user_id:
            return user_data[idx]['data']
    return None
