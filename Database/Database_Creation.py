import sqlite3

con = sqlite3.connect("test.db")
print("Connected to database \n")

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Users(User_ID INTEGER PRIMARY KEY, Username TEXT, First_Name TEXT, Last_Name TEXT, Password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS Events(User_ID INTEGER, Date TEXT, Start_Time TEXT, End_Time TEXT, FOREIGN KEY(User_ID) REFERENCES Users(User_ID))")


con.commit()
con.close()
