from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, User_Events, Groups, Group_Users_m2m
from flask_cors import CORS
from sqlite3 import IntegrityError
from sqlalchemy import select, between, or_, update, delete, text
from argon2 import PasswordHasher
from algorithm import superfn
import json

#initialize flask instance
app = Flask(__name__)
CORS(app)

#initialize and create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"
db.init_app(app)
with app.app_context():
    db.create_all()

#foreign key function to enable foreign key constraint
#call before each connection to database where you are inserting, updating, or deleting
def enable_foreign_key_constraint():
    db.session.execute(text("PRAGMA foreign_keys = ON"))
    
#user info on login endpoint
@app.route('/api/retrieve_user_info', methods=['GET', 'POST'])
def retrieve_user_info():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')

        if username is None:
            return jsonify({"success":False})
        
        userObj = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if userObj is None:
            return jsonify({'success': False})

        userID = userObj.User_ID
        groups = []
        for Groups in userObj.User_Groups:
            group_usernames = [Users.Username for Users in Groups.Group_Users]
            group_info = {
                "group_id": Groups.Group_ID,
                "group_name": Groups.Group_Name,
                "usernames": group_usernames
            }
            groups.append(group_info)

        information = {"user_id": userID, "groups": groups}
        return jsonify(information)

#Login and create account routes
@app.route('/api/login', methods = ['GET', 'POST'])
def handle_login():
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if username is None or password is None:
                return jsonify({"success":False})

            ph = PasswordHasher()
            stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
            if stmt is None:
                return jsonify({'success' : False})
            
            check_pass = False
            try:
                check_pass = ph.verify(stmt.Password, password)
            except: 
                pass
                
            if check_pass != True:
                return jsonify({'success' : False})    
            else:
                return jsonify({'success': True})
    
@app.route('/api/create_account', methods = ['GET','POST'])
def handle_create_account():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if username is None or first_name is None or last_name is None or password is None:
            return jsonify({"success":False})
        
        stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if stmt is None:
            ph = PasswordHasher()
            hashed_password = ph.hash(password)
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = hashed_password)
            enable_foreign_key_constraint()
            try:
                db.session.add(user)
            except:
                return jsonify({'success': False})
            db.session.commit()
            return jsonify({'success' : True})
        else:
            return jsonify({'success' : False})
        
#calendar event routes
@app.route('/api/create_event', methods = ['GET', 'POST'])
def create_event():
        if request.method == 'POST':
            data = request.json
            user_id = data.get('user_id')
            event_name = data.get('event_name')
            start_time = data.get('start_time')
            end_time = data.get('end_time')

            if user_id is None or event_name is None or start_time is None or end_time is None:
                return jsonify({"success":False})

            if not (user_id or event_name or start_time or end_time):
                return jsonify({"success":False})
            
            calendar_event = db.session.scalars(select(User_Events).where(User_Events.User_ID == user_id).where(or_(between(User_Events.Start_Time, start_time, end_time), between(User_Events.End_Time, start_time, end_time)))).first()

            if calendar_event is None:
                enable_foreign_key_constraint()
                event_to_add = User_Events(User_ID = user_id, Event_Name = event_name, Start_Time = start_time, End_Time = end_time)
                try:
                    db.session.add(event_to_add)
                except:
                    return jsonify({'success': False})
                db.session.commit()
                return jsonify({'success' : True})    
            else:
                return jsonify({'success' : False})

@app.route('/api/edit_event', methods = ['GET', 'POST'])
def edit_event():
    if request.method == "POST":
        data = request.json
        event_id = data.get("event_id")
        user_id = data.get("user_id")
        event_name = data.get("event_name")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if event_id is None or user_id is None or event_name is None or start_time is None or end_time is None:
            return jsonify({"success":False})

        enable_foreign_key_constraint()
        try:
            event = db.session.execute(update(User_Events).where(User_Events.Event_ID == event_id).where(User_Events.User_ID == user_id).values(Event_Name = event_name, Start_Time = start_time, End_Time = end_time))
        except:
            return jsonify({'success': False})
        if event.rowcount == 0:
            return jsonify({'success' : False})    
        else:
            db.session.commit()
            return jsonify({'success' : True})
    
@app.route('/api/delete_event', methods = ['GET', 'POST'])
def delete_event():
    if request.method == "POST":
        data = request.json
        event_id = data.get("event_id")
        user_id = data.get("user_id")

        if event_id is None or user_id is None:
            return jsonify({"success":False})

        try:
            delete_event = db.session.execute(delete(User_Events).where(User_Events.User_ID == user_id).where(User_Events.Event_ID == event_id))
        except:
            return jsonify({'success': False})
        if delete_event.rowcount == 0:
            return jsonify({'success' : False})
        else:
            db.session.commit()
            return jsonify({'success' : True})

#group free times and retrieve user events endpoints
@app.route("/api/retrieve_group_free_times", methods = ["GET", "POST"])
def retrieve_group_free_times():
    if request.method == "POST":
        data = request.json
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        group_id = data.get("group_id")

        if start_time is None or end_time is None or group_id is None:
            return jsonify({"success":False})

        #list of tuples to store user events
        user_events = []
        #add tuple of start time to list
        start_time_tuple = (start_time, start_time)
        user_events.append(start_time_tuple)
        #search for group with group id
        rc = db.session.scalars(select(Groups).where(Groups.Group_ID == group_id)).first()
        
        #if no group is found return false
        if rc is None:
            return jsonify({"success":False})
        #iterate through each user in the group
        for Users in rc.Group_Users:
            #iterate through the events of each user and append the event's (start time, end time) as a tuple to the user events list
            for User_Events in Users.Events_of_User:
                events = (User_Events.Start_Time, User_Events.End_Time)
                user_events.append(events)
        #append the end time to the list
        user_events.append((end_time, end_time))

        #pass the list to the algorithm
        free_times_list = superfn(user_events)
        
        #return the array of json objects
        return free_times_list
    
@app.route("/api/retrieve_user_events", methods = ["GET", "POST"])
def retrieve_user_events():
    if request.method == "POST":
        data = request.json
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        user_id = data.get("user_id")

        if user_id is None:
            return jsonify({"success":False})

        #list to store json objects for each events
        user_events = []
        
        #find user with matching user id
        rc = db.session.scalars(select(Users).where(Users.User_ID == user_id)).first()

        #if no user found return false
        if rc is None:
            return jsonify({"success":False})
        
        #iterate through the events of user list and for each event create a json object and append to the list
        for User_Events in rc.Events_of_User:
            events_json = {"title" : User_Events.Event_Name, "start" : User_Events.Start_Time, "end" : User_Events.End_Time, "allDay" : False, "id" : User_Events.Event_ID}
            user_events.append(events_json)

        #return false if no events
        if not user_events:
            return jsonify({"success":False})
        
        #return the array of json objects
        return jsonify(user_events)

#group endpoints
@app.route('/api/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        group_name = data.get('group_name')

        if user_id is None or group_name is None:
            return jsonify({"success":False})

        group = Groups(Group_Name=group_name)
        enable_foreign_key_constraint()
        try:
            db.session.add(group)
            db.session.commit()
        except:
            return jsonify({'success': False})
        try:
            group_id = db.session.execute(text("SELECT last_insert_rowid()")).scalar()
            db.session.execute(Group_Users_m2m.insert().values(User_ID = user_id, Group_ID = group_id))
            db.session.commit()
        except:
            return jsonify({'success': False, 'group_id': group_id})
        
        return jsonify({'success': True})

@app.route('/api/add_users_group', methods=['GET', 'POST'])
def addToGroup():
    if request.method == 'POST':
        data = request.json
        name = data.get('username')
        group_id = data.get('group_id')

        if name is None or group_id is None:
            return jsonify({"success":False})

        user = db.session.scalars(select(Users).where(Users.Username == name)).first()
        if user is None:
            return jsonify({'success': False})
        user_id = user.User_ID
        g = db.session.scalars(select(Groups).where(Groups.Group_ID == group_id)).first()
        if g is None:
            return jsonify({'success': False})
        
        try:
            enable_foreign_key_constraint()
            db.session.execute(text("INSERT INTO Groups_Users (User_ID, Group_ID) VALUES (:User_ID, :Group_ID)"), {'User_ID': user_id, 'Group_ID': group_id})
        except:
            return jsonify({'success': False})
        db.session.commit()
        return jsonify({'success': True})

@app.route('/api/delete_user_group', methods=['GET', 'POST'])
def removeFromGroup():
    data = request.json
    name = data.get('username')
    group_id = data.get('group_id')

    if name is None or group_id is None:
        return jsonify({"success":False})

    user = db.session.scalars(select(Users).where(Users.Username == name)).first()
    if user is None or group_id is None:
        return jsonify({'success': False})
    else:
        user_ID = user.User_ID
        db.session.execute(text("DELETE FROM Groups_Users WHERE User_ID=:user_id AND Group_ID = :group_id"),
                           {'user_id': user_ID, 'group_id': group_id})
        db.session.commit()
    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(debug = True)
