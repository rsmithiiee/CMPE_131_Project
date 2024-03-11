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

#RESOURCES
#https://www.programiz.com/python-programming/time <-time lib documentation we porob need later\
#https://www.programiz.com/python-programming/datetime/strptime <-also very useful
def generateEvent(startTime, endTime):
  if request.method=='ADD_EVENT':
    dt_start = datetime.strptime(startTime, "%d/%m/%Y %H:%M:%S")#start time?
    dt_end = datetime.strptime(endTime, "%d/%m/%Y %H:%M:%S")
    return
  else:
    #check for event in db and delete, how tf do I find an event???
    return

#calendar_list should be a list of tuples with start and end times [ {s1, e1}, {s2, e2} , etc]
def generateFreeTimes(calender_list):
  for timeTuple in calendar_list:
    #wtf format am I using here? strings? unix? I need to know
    start = timeTuple[0]
    end = timeTuple[1]
    #do math??? check to see if we cant just display occupied times instead
  
  return render.template('/')#url redirect I think, or a render display go figure

if __name__ == "__main__":
  app.run(debug=True)
