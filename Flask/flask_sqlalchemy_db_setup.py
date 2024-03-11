from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///official.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class = Base)

class Users(db.Model):
    __tablename__ = "Users"
    User_ID : Mapped[int] = mapped_column(primary_key = True)
    First_Name : Mapped[str]
    Last_Name : Mapped[str]
    Username : Mapped[str] = mapped_column(unique = True, nullable = False)
    Password : Mapped[str]

class User_Events(db.Model):
    __tablename__ = "User_Events"
    Event_ID : Mapped[int] = mapped_column(primary_key = True)
    User_ID : Mapped[int] = mapped_column(ForeignKey("Users.User_ID"))
    Event_Name : Mapped[str]
    Start_Time : Mapped[str]
    End_Time : Mapped[str]

class Groups(db.Model):
    __tablename__ = "Groups"
    Group_ID : Mapped[int] = mapped_column(primary_key = True)
    Group_Name : Mapped[str]

class Group_Events(db.Model):
    __tablename__ = "Group Events"
    Event_ID : Mapped[int] = mapped_column(primary_key = True)
    Group_ID : Mapped[int]
    Start_Time : Mapped[str]
    End_Time : Mapped[str]

group_users_m2m = db.Table(
    "Group_Users",
    sa.Column("User_ID", sa.ForeignKey(Users.User_ID), primary_key = True),
    sa.Column("Group_ID", sa.ForeignKey(Groups.Group_ID), primary_key = True),
)

with app.app_context():
    db.create_all()
