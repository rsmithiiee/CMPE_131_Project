from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import datetime

#setup?
app = Flask(__name__)
#relative path ig? insert whatever file when needed (i.e user.db or group.db) <-this creates a db apparently
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///insert_db_name_here.db'
db = SQLAlchemy(app)

#no idea what this does (likely creates an event in db with a description and timestamp), just for practice , may be useful in the future
class WTFisThis(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(100, nullable = False))
  date_created = db.Column(db.DateTime(default.datetime.utcnow))
  def __repr__ (self):
    return '<Event %r>' % self.id


#set a form+action on our frontend with the corresponding methods for event creation
#prob gonna need more methods for group creation, friend adding, all that fun stuff
@app.route("/", methods=['ADD_EVENT', 'DELETE_EVENT'])
#https://www.programiz.com/python-programming/time <-time lib documentation we porob need later
def generateEvent(dateTime):
  if request.method=='ADD_EVENT':
    pass #todo add calendar event
  else:
    pass #todo remove calendar event if present

#calendar_list should be a list of tuples with start and end times [ {s1, e1}, {s2, e2} , etc]
def generateFreeTimes(calender_list):
    #do things, no idea how data is gonna be passed but we'll see
  return render.template('/')#url redirect I think, or a render display go figure

if __name__ == "__main__":
  app.run(debug=True)
