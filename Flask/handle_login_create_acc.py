from flask import Flask, request, Blueprint
import flask_sqlalchemy_db_setup

login_bp = Blueprint('login_bp', __name__)
@login_bp.route('/handle_login', method = ['GET','POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userObj = flask_sqlalchemy_db_setup.Users.query.get(username)
        if userObj.Password == password and userObj is not None:
            # flask_sqlalchemy_db_setup.db.add_user(userObj)
            # flask_sqlalchemy_db_setup.db.session.commit()
            return True
        else:
            return False
@login_bp.route('/handle_create_account', method = ['POST'])
def handle_create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email_address']
        password = request.form['password']
        first = request.form['first_name']
        last = request.form['last_name']

        userObj = flask_sqlalchemy_db_setup.Users.query.get(username)

        if userObj is None:
            new_item = User(None,first,last,username,password)
            flask_sqlalchemy_db_setup.db.insert(new_item)
            flask_sqlalchemy_db_setup.db.session.commit()
            return True
        else:
            return False
    
