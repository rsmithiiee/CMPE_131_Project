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
            data = request.json
            username = data.get('username')
            password = data.get('password')

            ph = PasswordHasher()
            hashed_password = ph.hash(password)
            stmt = db.session.scalars(select(Users).where(Users.Username == username).where(Users.Password == hashed_password)).first()
            check_pass = ph.verify(stmt.Password, password)

        if stmt is None or check_pass != True:
            return jsonify({'success': False})    
        else:
            return jsonify({'success': True})
    
@app.route('/create_account', methods = ['GET','POST'])
def handle_create_account():
    if request.method == 'POST':
        data = request.json()
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        
        stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if stmt is None:
            ph = PasswordHasher()
            hashed_password = ph.hash()
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': False})
        else:
            return jsonify({'success': True})

@app.route('api/create_group', methods = ['GET','POST'])
def create_group():
    if request.method == 'POST':
        data = request.json
        ID = data.get('user_id')
        group_name = data.get('group_name')
        group = Groups(Group_Name = group_name)
        #TODO: Get group ID after it has been added to group Table
        db.session.add(group)
        group_id = db.session.execute("SELECT last_insert_rowid()")
        input = group_users_m2m(User_ID = ID, Group_ID = group_id)
        db.session.add(input)
        #db.session.execute("INSERT INTO Group_Users (User_ID, Group_ID) VALUES (?,?)", (ID, group_ID))
        db.session.commit()
    return jsonify({'success': True})

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

