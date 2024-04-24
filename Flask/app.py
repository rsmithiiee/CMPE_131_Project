from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, User_Events, Groups, Group_Users_m2m
from flask_cors import CORS
from sqlalchemy import select, between, or_, update, delete, text
from argon2 import PasswordHasher

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

#Login and create account routes
@app.route('/api/login', methods = ['GET', 'POST'])
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
    
@app.route('/api/create_account', methods = ['GET','POST'])
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
            hashed_password = ph.hash(password)
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = hashed_password)
            enable_foreign_key_constraint()
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': False})
        else:
            return jsonify({'success': True})

#calendar event routes
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
            enable_foreign_key_constraint()
            event_to_add = User_Events(User_ID = user_id, Event_Name = event_name, Start_Time = start_time, End_Time = end_time)
            db.session.add(event_to_add)
            db.session.commit()
            return jsonify({'success': True})    
        else:
            return jsonify({'success': False})
@app.route('/api/create_event', methods = ['GET', 'POST'])
def create_event():
        if request.method == 'POST':
            data = request.json
            user_id = data.get('user_id')
            event_name = data.get('event_name')
            start_time = data.get('start_time')
            end_time = data.get('end_time')

        calendar_event = db.session.scalars(select(User_Events).where(or_(between(User_Events.Start_Time, start_time, end_time), between(User_Events.End_Time, start_time, end_time)))).first()

        if calendar_event is None:
            enable_foreign_key_constraint()
            event_to_add = User_Events(User_ID = user_id, Event_Name = event_name, Start_Time = start_time, End_Time = end_time)
            db.session.add(event_to_add)
            db.session.commit()
            return jsonify({'success': True})    
        else:
            return jsonify({'success': False})

@app.route('/api/edit_event', methods = ['GET', 'POST'])
def edit_event():
    if request.method == 'POST':
        data = request.json()
        event_id = data.get("event_id")
        user_id = data.get("user_id")
        event_name = data.get("event_name")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

    enable_foreign_key_constraint()
    event = db.session.execute(update(User_Events).where(User_Events.Event_ID == event_id).where(User_Events.User_ID == user_id).values(Event_Name = event_name, Start_Time = start_time, End_Time = end_time))

    if event.rowcount == 0:
        return jsonify({'success': False})    
    else:
        db.session.commit()
        return jsonify({'success': True})
        

if __name__ == "__main__":
    app.run(debug = True)
