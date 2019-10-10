from flask import render_template
from app import app
from app.controller import gen_ovpn
from app.ldapreq.controller import get_users_displayName, get_users_sAMAccountName

@app.route('/')
def index():
    users_dn = get_users_displayName()
    users_sAMA = get_users_sAMAccountName()
    result_table = list(zip(users_dn, users_sAMA))
    gen_ovpn(users_sAMA)
    return render_template(
        'index.html',
        title = 'User List',
        user_table = result_table
    )