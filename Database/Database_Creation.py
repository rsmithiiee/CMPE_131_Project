import sqlite3

con = sqlite3.connect("test.db")
print("Connected to database \n")

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Users(User_ID INTEGER PRIMARY KEY, First_Name TEXT, Last_Name TEXT, Username TEXT NOT NULL UNIQUE, Password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS Events(User_ID INTEGER, Event_Name TEXT, Start_Time TEXT, End_Time TEXT, FOREIGN KEY(User_ID) REFERENCES Users(User_ID))")
cur.execute("CREATE TABLE IF NOT EXISTS Groups(Group_ID INTEGER PRIMARY KEY, Group_Name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS Groups_Users(Group_ID INTEGER, User_ID INTEGER, FOREIGN KEY(Group_ID) REFERENCES Groups(Group_ID), FOREIGN KEY(User_ID) REFERENCES Users(User_ID))")
cur.execute("CREATE TABLE IF NOT EXISTS  Group_Events(Group_ID INTEGER, Start_Time TEXT, End_Time TEXT, FOREIGN KEY(Group_ID) REFERENCES Groups)")

con.commit()
con.close()
