from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

Group_Users_m2m = Table(
    "Groups_Users",
    Base.metadata,
    Column("Groups", ForeignKey("Groups.Group_ID"), primary_key = True),
    Column("Users", ForeignKey("Users.User_ID"), primary_key = True),
)

class Users(db.Model):
    __tablename__ = "Users"
    User_ID : Mapped[int] = mapped_column(primary_key = True)
    First_Name : Mapped[str]
    Last_Name : Mapped[str]
    Username : Mapped[str] = mapped_column(unique = True)
    Password : Mapped[str]
    User_Groups : Mapped[List["Groups"]] = relationship(secondary = Group_Users_m2m, back_populates = "Group_Users")
    Events_of_User : Mapped[List["User_Events"]] = relationship()

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
    Group_Users : Mapped[List["Users"]] = relationship(secondary = Group_Users_m2m, back_populates = "User_Groups")
