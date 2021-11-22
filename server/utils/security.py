import hashlib


def encode_user_agent(user_agent):
    return hashlib.md5(str.encode(user_agent)).hexdigest()
