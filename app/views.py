from flask import render_template

from app import app
from app.controller import get_users_sAMAccountName


@app.route('/')
def index():
    return render_template(
        'index.html',
        title = 'User List',
        users = get_users_sAMAccountName()
    )