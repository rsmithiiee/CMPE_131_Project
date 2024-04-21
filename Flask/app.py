from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, Groups, group_users_m2m
# from flask_cors import CORS
import sqlite3
from sqlalchemy import select

# from argon2 import PasswordHasher

# initialize flask instance
app = Flask(__name__)

# initialize and create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"
db.init_app(app)
with app.app_context():
    db.create_all()


# Login and create account routes
@app.route('/api/login', methods=['GET', 'POST'])
def handle_login():
        if request.method == 'POST':
            if request.method == 'POST':
                data = request.get_json()
                username = data['username']
                password = data['password']
                stmt = db.session.scalars(
                    select(Users).where(Users.Username == username).where(Users.Password == password)).first()
                # ph = PasswordHasher
                # check_pass = ph.verify(stmt.Password, password)
                # or check_pass != True
            if stmt is None:
                return jsonify({'success': False, 'message': 'Login failed'})
            else:
                return jsonify({'success': True, 'message': 'Login successful'})
    
# @app.route('/create_account', methods = ['GET','POST'])
# def handle_create_account():
#     if request.method == 'POST':
#         data = request.json()
#         username = data.get('username')
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         password = data.get('password')
#
#         stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
#         if stmt is None:
#             # ph = PasswordHasher()
#             # hashed_password = ph.hash()
#             user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = password)


@app.route('/api/create_account', methods=['GET', 'POST'])
def handle_create_account():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = data['password']
        # ph = PasswordHasher()
        # hashed_password = ph.hash()

        stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if stmt is None:
            user = Users(First_Name=first_name, Last_Name=last_name, Username=username, Password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': False})
        else:
            return jsonify({'success': True})

#group handling
@app.route('/api/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        data = request.json
        ID = data.get('user_id')
        group_name = data.get('group_name')
        group = Groups(Group_Name=group_name)
        db.session.add(group)
        group_id = db.session.execute("SELECT last_insert_rowid()")
        input = group_users_m2m(User_ID=ID, Group_ID=group_id)
        db.session.add(input)
        # db.session.execute("INSERT INTO Group_Users (User_ID, Group_ID) VALUES (?,?)", (ID, group_ID))
        db.session.commit()
    return jsonify({'success': True})


@app.route('/api/add_users_group', methods=['GET', 'POST'])
def addToGroup():
    if request.method == 'POST':
        data = request.json
        name = data.get('username')
        user = db.session.scalars(select(Users).where(Users.Username == name)).first()
        if user is None:
            return jsonify({'success': False, 'message': 'User not found!'})
        else:
            # TODO: How to retrieve group ID from DB
            user_id = user.USER_ID
            group_id = db.session.execute("SELECT Group_ID from Group_Users WHERE User_ID = user_id", {"user_id": user_id}).first()
            if group_id is None:
                return jsonify({'success': False})
            group_entry = group_users_m2m.insert().values(User_ID=user_id, Group_ID=group_id)
            db.session.add_all(group_entry)
            db.session.commit()
    return jsonify({'success': True})


@app.route('/api/delete_user_group', methods=['POST'])
def removeFromGroup():
    data = request.json
    name = data.get('username')
    user = db.session.scalars(select(Users).where(Users.Username == name)).first()
    if user is None:
        return jsonify({'success': False})
    else :
        user_ID = user.USER_ID
        group_id = db.session.execute("SELECT Group_ID from Group_Users WHERE User_ID = user_id", {'user_id': user_ID}).first()
        db.session.execute("DELETE FROM Group_Users WHERE User_ID = user_ID AND Group_ID = group_id", {'group_id': group_id}).first()
        db.session.commit()
    return jsonify({'success': True})

#event handling
@app.route('/api/create_event', methods = ['GET', 'POST'])
def create_event():
        if request.method == 'POSt':
            data = request.json
            user_id = data.get['user_id']
            event_name = data.get['event_name']
            start_time = data.get['start_time']
            end_time = data.get['end_time']

        calendar_event = db.session.scalars(select(User_Events).where(or_(between(User_Events.Start_Time, start_time, end_time), between(User_Events.End_Time, start_time, end_time)))).first()

        if calendar_event is None:
            db.session.add(calendar_event)
            db.session.commit()
            return jsonify({'success': True})    
        else:
            return jsonify({'success': False})

if __name__ == "__main__":
    app.run(debug=True)
