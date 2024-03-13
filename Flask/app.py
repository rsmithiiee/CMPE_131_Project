from flask import Flask
from flask_sqlalchemy_db_setup import db, Users
from handle_login_create_acc import login_bp
from flask_cors import CORS
from sqlalchemy import select

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(login_bp)

@app.route('/test')
def check_login():
    username = 'test'
    password = 'test'
    result = db.session.execute(select(Users).filter_by(Users.User_ID)).first()       

    result.all()

if __name__ == "__main__":
    app.run(debug = True)
