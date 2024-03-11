from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy_db_setup import db, Users

login_bp = Blueprint('login', __name__)
create_account_bp = Blueprint('create_account', __name__)

@login_bp.route('/handle_login', method = ['POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.execute(select(Users).where(Users.Username == username, Users.Password == password))

        if(user):
            return "login successful"
        else:
            return "incorrect username or password"

@create_account_bp.route('/handle_create_account', method = ['POST'])
def handle_create_account():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_id = request.form['user_id']
        password = request.form['password']
    
