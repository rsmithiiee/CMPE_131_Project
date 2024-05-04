from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, User_Events, Groups, Group_Users_m2m
from flask_cors import CORS
from sqlite3 import IntegrityError
from sqlalchemy import select, between, or_, update, delete, text
from argon2 import PasswordHasher
from algorithm import superfn

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

#Login and create account routes
@app.route('/api/login', methods = ['GET', 'POST'])
def handle_login():
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            password = data.get('password')

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
        
        stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if stmt is None:
            ph = PasswordHasher()
            hashed_password = ph.hash(password)
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = hashed_password)
            enable_foreign_key_constraint()
            db.session.add(user)
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

            calendar_event = db.session.scalars(select(User_Events).where(User_Events.User_ID == user_id).where(or_(between(User_Events.Start_Time, start_time, end_time), between(User_Events.End_Time, start_time, end_time)))).first()

            if calendar_event is None:
                enable_foreign_key_constraint()
                event_to_add = User_Events(User_ID = user_id, Event_Name = event_name, Start_Time = start_time, End_Time = end_time)
                db.session.add(event_to_add)
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

        enable_foreign_key_constraint()
        event = db.session.execute(update(User_Events).where(User_Events.Event_ID == event_id).where(User_Events.User_ID == user_id).values(Event_Name = event_name, Start_Time = start_time, End_Time = end_time))

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

        delete_event = db.session.execute(delete(User_Events).where(User_Events.User_ID == user_id).where(User_Events.Event_ID == event_id))

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

        #list to store json objects for each events
        user_events = []
        
        #find user with matching user id
        rc = db.session.scalars(select(Users).where(Users.User_ID == user_id)).first()

        #if no user found return false
        if rc is None:
            return jsonify({"success":False})
        
        #iterate through the events of user list and for each event create a json object and append to the list
        for User_Events in rc.Events_of_User:
            events_json = {"Title" : User_Events.Event_Name, "start" : User_Events.Start_Time, "end" : User_Events.End_Time, "allDay" : False, "id" : User_Events.Event_ID}
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
            return jsonify({'success': False})
        
        return jsonify({'success': True})

@app.route('/api/add_users_group', methods=['GET', 'POST'])
def addToGroup():
    if request.method == 'POST':
        data = request.json
        name = data.get('username')
        group_id = data.get('group_id')
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
    if request.method == 'POST':
        data = request.json
        name = data.get('username')
        group = data.get('group_name')
        user = db.session.scalars(select(Users).where(Users.Username == name)).first()
        if user is None:
            return jsonify({'success': False})
        else :
            user_ID = user.User_ID
            group = db.session.scalars(select(Groups).where(Groups.Group_Name == group)).first()
            group_id = group.Group_ID
            db.session.execute(text("DELETE FROM Group_Users WHERE User_ID=:user_id AND Group_ID = :group_id"), {'user_id': user_ID, 'group_id': group_id})
            db.session.commit()
            return jsonify({'success': True})


if __name__ == "__main__":
    app.run(debug = True)