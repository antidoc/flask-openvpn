import os
# from app.ldapreq.controller import get_users_sAMAccountName
from app.gencert.controller import gen_cert

# users = get_users_sAMAccountName()
users = ['shaman']
def gen_ovpn(users):
    for user in users:
        if not os.path.exists('static/certs/' + user + '.ovpn'):
            gen_cert(user)