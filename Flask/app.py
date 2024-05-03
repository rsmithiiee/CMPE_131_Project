from sqlite3 import IntegrityError
from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, Groups, Group_Users_m2m
import sqlite3
from flask import Flask, request, jsonify, sessions
from flask_sqlalchemy_db_setup import db, Users, User_Events, Groups
# from flask_cors import CORS
from sqlalchemy import select, between, or_, update, delete, text
from argon2 import PasswordHasher
import json

# from argon2 import PasswordHasher

# initialize flask instance
app = Flask(__name__)

# initialize and create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"
db.init_app(app)
with app.app_context():
    db.create_all()


def enable_foreign_key_constraint():
    db.session.execute(text("PRAGMA foreign_keys = ON"))


def listUserEvents(startTime, endTime, userID):
    event_list = db.session.scalars(
        select(User_Events).where(User_Events.User_ID == userID).where(User_Events.Start_Time == startTime).where(
            User_Events.End_Time == endTime)).all()
    if (len(event_list) == 0):
        return jsonify({'success': False, 'message': 'No scheduled events'})
    # change heading for data
    return json.dumps(event_list)


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


# group handling
@app.route('/api/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        group_name = data.get('group_name')
        group = Groups(Group_Name=group_name)
        enable_foreign_key_constraint()
        db.session.add(group)
        group_id = db.session.execute(text("SELECT last_insert_rowid()")).scalar()
        db.session.execute(text("INSERT INTO Group_Users (User_ID, Group_ID) VALUES (:User_ID, :Group_ID)"),
                           {'User_ID': user_id, 'Group_ID': group_id})

        db.session.commit()
    return jsonify({'success': True})


@app.route('/api/test', methods=['GET', 'POST'])
def test_user():
    name = 'hemanthkarnati'
    group = 'Embedded'
    user = db.session.scalars(select(Users).where(Users.Username == name)).first()
    if user is None:
        return jsonify({'success': False})
    else:
        user_ID = user.User_ID
        group = db.session.scalars(select(Groups).where(Groups.Group_Name == group)).first()
        group_id = group.Group_ID
        db.session.execute(text("DELETE FROM Group_Users WHERE User_ID=:user_id AND Group_ID = :group_id"),
                           {'user_id': user_ID, 'group_id': group_id})
        db.session.commit()
    return jsonify({'success': True})


@app.route('/api/add_users_group', methods=['GET', 'POST'])
def addToGroup():
    if request.method == 'POST':
        data = request.json
        name = data.get('username')
        group = data.get('group_name')
        user = db.session.scalars(select(Users).where(Users.Username == name)).first()
        if user is None:
            return jsonify({'success': False})
        else:
            g = db.session.scalars(select(Groups).where(Groups.Group_Name == group)).first()
            group_id = g.Group_ID
            user_id = user.User_ID
            if group_id is None:
                return jsonify({'success': False})
            try:
                enable_foreign_key_constraint()
                db.session.execute(text("INSERT INTO Group_Users (User_ID, Group_ID) VALUES (:User_ID, :Group_ID)"),
                                   {'User_ID': user_id, 'Group_ID': group_id})
            except (IntegrityError) as e:
                return jsonify({'success': False})
            db.session.commit()
    return jsonify({'success': True})


@app.route('/api/delete_user_group', methods=['GET', 'POST'])
def removeFromGroup():
    data = request.json
    name = data.get('username')
    group = data.get('group_name')
    user = db.session.scalars(select(Users).where(Users.Username == name)).first()
    if user is None:
        return jsonify({'success': False})
    else:
        user_ID = user.User_ID
        group = db.session.scalars(select(Groups).where(Groups.Group_Name == group)).first()
        group_id = group.Group_ID
        db.session.execute(text("DELETE FROM Group_Users WHERE User_ID=:user_id AND Group_ID = :group_id"),
                           {'user_id': user_ID, 'group_id': group_id})
        db.session.commit()
    return jsonify({'success': True})


# event handling
@app.route('/api/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        data = request.json
        user_id = data.get['user_id']
        event_name = data.get['event_name']
        start_time = data.get['start_time']
        end_time = data.get['end_time']

    calendar_event = db.session.scalars(select(User_Events).where(
        or_(between(User_Events.Start_Time, start_time, end_time),
            between(User_Events.End_Time, start_time, end_time)))).first()

    if calendar_event is None:
        enable_foreign_key_constraint()
        event_to_add = User_Events(User_ID=user_id, Event_Name=event_name, Start_Time=start_time, End_Time=end_time)
        db.session.add(event_to_add)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/api/retrieve_user_events', methods=['GET', 'POST'])
def retrieve_user_events():
    if request.method == 'POST':
        data = request.json
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        username = data.get('username')
        user_id = db.session.scalars(select(Users).where(Users.Username == username)).first()
        return listUserEvents(start_time, end_time, user_id)


@app.route('/api/retreive_user_info', methods=['GET', 'POST'])
def retreive_user_info():
    information = {}
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        userObj = db.session.scalars(select(Users).where(Users.Username == username)).first()
        userID = userObj.User_ID
        information = {
            "user_id": userID,
            "groups": [
                {
                    "group_id": group.Group_ID,
                    "group_name": group.Group_Name,
                    "usernames": [{"username": user.User_ID} for user in group.Users]
                }
                for group in userObj.Groups
            ]
        }
    return json.dumps(information)



if __name__ == "__main__":
    app.run(debug=True)
