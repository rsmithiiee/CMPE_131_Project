from flask import Flask, request, jsonify
from flask_sqlalchemy_db_setup import db, Users
from flask_cors import CORS
import sqlite3
from sqlalchemy import select
from argon2 import PasswordHasher

#initialize flask instance
app = Flask(__name__)
CORS(app)

#initialize and create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"
db.init_app(app)
with app.app_context():
    db.create_all()

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
            hashed_password = ph.hash()
            user = Users(First_Name = first_name, Last_Name = last_name, Username = username, Password = hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': False})
        else:
            return jsonify({'success': True})
        

if __name__ == "__main__":
    app.run(debug = True)
