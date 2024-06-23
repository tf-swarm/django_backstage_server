import jwt


#解密token
def decode_token(token):
    user = []
    user.append(jwt.decode(token, 'secret_key', algorithms=['HS256'])['username'])
    user.append(jwt.decode(token, 'secret_key', algorithms=['HS256'])['password'])
    return user


#生成token
def encode_token(username,password):
    token = jwt.encode(
        {
            'username': username,
             'password': password
        },
        'secret_key',
        algorithm='HS256').decode('utf-8')
    return token
