from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users, Groups
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
            username = request.form['username']
            password = request.form['password']
            stmt = db.session.scalars(select(Users).where(Users.Username == username).where(Users.Password == password)).first()
        if stmt is None:
            return jsonify({'success': False, 'message': 'Login failed'})    
        else:
            return jsonify({'success': True, 'message': 'Login successful'})
    
@app.route('/create_account', methods = ['GET','POST'])
def handle_create_account():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        stmt = db.session.scalars(select(Users).where(Users.Username == username)).first()
        if stmt is None:
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = password)
            db.session.add(user)
            db.session.commit()
        else:
            return jsonify({'success': False, 'message': 'Username taken'})

@app.route('api/create_group', methods = ['GET','POST'])
def create_group():
    if request.method == 'POST':
        ID = request.form['user_id']
        group_name = request.form['group_name']
        group = Groups(Group_Name = group_name)
        db.session.add(group)
        db.session.commit()
        #TODO: finish code

    return jsonify({'success': True, 'message': 'Group Created!'})

@app.route('api/add_users_group', methods = ['GET','POST'])
def addToGroup():
    if request.method == 'POST':
        name = request.form['username']
        #TODO: Finish code



if __name__ == "__main__":
    app.run(debug = True)
