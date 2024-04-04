from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, Groups, group_users_m2m
# from flask_cors import CORS
import sqlite3
from sqlalchemy import select
#from argon2 import PasswordHasher

#initialize flask instance
app = Flask(__name__)

#initialize and create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"
db.init_app(app)
with app.app_context():
    db.create_all()

#Login and create account routes
@app.route('/login', methods = ['GET', 'POST'])
def handle_login():
        if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            password = data['password']
            stmt = db.session.scalars(select(Users).where(Users.Username == username).where(Users.Password == password)).first()
            ph = PasswordHasher
            check_pass = ph.verify(stmt.Password, password)
        if stmt is None or check_pass != True:
            return jsonify({'success': False, 'message': 'Login failed'})    
        else:
            return jsonify({'success': True, 'message': 'Login successful'})
    
@app.route('/create_account', methods = ['GET','POST'])
def handle_create_account():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = data['password']
        ph = PasswordHasher()
        hashed_password = ph.hash()
        
        stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if stmt is None:
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Account was created'})
        else:
            return jsonify({'success': False, 'message': 'Could not create account'})

@app.route('api/create_group', methods = ['GET','POST'])
def create_group():
    if request.method == 'POST':
        data = request.json
        ID = data.get('user_id')
        group_name = data.get('group_name')
        group = Groups(Group_Name = group_name)
        db.session.add(group)
        db.session.commit()
        #TODO: finish code

    return jsonify({'success': True, 'message': 'Group Created!'})

@app.route('api/add_users_group', methods = ['GET','POST'])
def addToGroup():
    if request.method == 'POST':
        data = request.json
        name = data.get('username')
        user = db.session.scalars(select(Users).where(Users.Username == name)).first()
        group = db.session.scalars(select(Groups).where(Groups.Group_Name == name)).first()
        if user or group is None:
            return jsonify({'success': False, 'message': 'User/Group not found!'})
        else:
            #TODO: How to retrieve group ID from DB
            user_id = user.USER_ID
            group_id = group.GROUP_ID
            group_entry = group_users_m2m.insert().values(User_ID=user_id, Group_ID=group_id)
            db.session.add_all(group_entry)
            db.session.commit()
    return jsonify({'success': True, 'message': 'Group Info Updated'})

@app.route('api/delete_user_group', methods = ['POST'])
def removeFromGroup():
    return jsonify({'success': True, 'message': 'User successfully deleted!'})

if __name__ == "__main__":
    app.run(debug = True)
