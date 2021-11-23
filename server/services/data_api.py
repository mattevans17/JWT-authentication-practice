user_data = [{
    'user_id': '123',
    'data': {
        'cars': [
            {
                'firm': 'Koenigsegg',
                'model': 'Regera'
            }
        ]
    }
}]


# def add_data(user_id, data):
#     for idx in range(len(user_data)):
#         if user_data[idx]['user_id'] == user_id:
#             user_data[idx]['data'] = data
#             return
#     user_data['user_id'] = user_id
#     user_data['data'] = data


def get_data(user_id):
    for idx in range(len(user_data)):
        if user_data[idx]['user_id'] == user_id:
            return user_data[idx]['data']
    return None
