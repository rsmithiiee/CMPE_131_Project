
#note: must use functions in this order: stringtodatetime, supersort, removeoverlap, freetimeinday
from datetime import datetime
import json
def superfn(time_list):
    stringToDatetime(time_list)
    superSort(time_list)
    removeOverlap(time_list)
    freetimelist = freeTimeInDay(time_list)
    convertToJson = [{'start': item[0], 'end': item[1]} for item in freetimelist]
    json_data = json.dumps(convertToJson)
    return json_data
#FOR RYAN AYAYAYAYAYAYA
#takes in 2 tuples of string dates in ISO. Returns true if no overlap, false if overlap
def cmpEvent(timeStringTupleOne, timeStringTupleTwo):
    dateTimeTupleOne = ("","")
    dateTimeTupleTwo = ("", "")
    dateTimeTupleOne = (datetime.strptime(timeStringTupleOne[0] , "%Y-%m-%d %H:%M:%S.%f"), datetime.strptime(timeStringTupleOne[1] , "%Y-%m-%d %H:%M:%S.%f"))
    dateTimeTupleTwo = (datetime.strptime(timeStringTupleTwo[0] , "%Y-%m-%d %H:%M:%S.%f"), datetime.strptime(timeStringTupleTwo[1] , "%Y-%m-%d %H:%M:%S.%f"))
    if(dateTimeTupleOne[0] <= dateTimeTupleTwo[0]):
        if(dateTimeTupleOne[1] >= dateTimeTupleTwo[1] and dateTimeTupleTwo[0] <= dateTimeTupleOne[1]):
            return False 
        elif (dateTimeTupleTwo[1] > dateTimeTupleOne[1] and dateTimeTupleTwo[0] <= dateTimeTupleOne[1]):
            return False
    if(dateTimeTupleTwo[0] <= dateTimeTupleOne[0]):
        if(dateTimeTupleTwo[1] >= dateTimeTupleOne[1] and dateTimeTupleOne[0] <= [1]):
            return False 
        elif (dateTimeTupleOne[1] > dateTimeTupleTwo[1] and dateTimeTupleOne[0] <= dateTimeTupleTwo[1]):
            return False
    return True
   
def freeTimeInDay(time_list):
   #convert from ISO 8601 to datetime obj and find length
  free_time_list = []#buffer for handling later
  #find gaps where event 1 end < event 2 start
  length = len(time_list)
  for i in range (1, length, 1):
    if(time_list[i - 1][1] < time_list[i][0]):
       free_time_list += [(time_list[i - 1][1], time_list[i][0])]
  return free_time_list

#use insertionsort since we have small datasets (<20)
#sort by start/end time (list of tuples of datetimes)
def sortByStartTime(time_list):
  for i in range(1, len(time_list), 1):
    pos = time_list[i]
    j = i -1
    while (j >= 0 and time_list[j][0] > pos[0]):
        time_list[j], time_list[j + 1] = time_list[j + 1], time_list[j]
        j = j - 1
def sortByEndTime(time_list):
   for i in range(1, len(time_list), 1):
    pos = time_list[i]
    j = i -1
    while (j >= 0 and time_list[j][1] > pos[1] and time_list[j][0] >= pos[0]):
        time_list[j], time_list[j + 1] = time_list[j + 1], time_list[j]
        j = j - 1

#for convenience
def superSort(time_list):
   sortByStartTime(time_list)
   sortByEndTime(time_list)

#converts all elements from iso string to datetime obj and return length of list
def stringToDatetime(time_list):
  timetuple = ("filler", "filler")
  for timeTuple in time_list:
    timetuple = (datetime.strptime(timeTuple[0] , "%Y-%m-%d %H:%M:%S.%f"), datetime.strptime(timeTuple[1] , "%Y-%m-%d %H:%M:%S.%f"))
  return len(time_list)

#remove overlapping times, requires sorted (start and end) datetime list and length of list
def removeOverlap(time_list):
  templist = []
  templist += time_list
  cleanedList = []
  for i in range (0, len(templist) - 1, 1):
      for j in range ( i + 1, len(templist), 1):
        if(templist[i][0] <= templist[j][0]):
          if(templist[i][1] >= templist[j][1] and templist[j][0] <= templist[i][1]):
            cleanedList += [j] 
          elif (templist[j][1] > templist[i][1] and templist[j][0] <= templist[i][1]):
            templist[i] = (templist[i][0],templist[j][1])
            cleanedList += [j]
  offset = 0
  list.sort(cleanedList)
  cleanedList = list(set(cleanedList))
  for i in cleanedList:
    templist.remove(templist[i - offset])
    offset += 1
  return templist#uhhh ignore the naming yep

#main for testing
#def main():
 #   time_list =[("2022-09-27 18:00:00.000", "2022-09-27 23:00:00.000"),("2022-09-27 00:00:00.000", "2022-09-27 10:00:00.000"),("2022-09-26 00:00:00.000", "2022-09-27 03:00:00.000"),("2023-09-28 04:00:00.000","2023-09-29 18:00:00.000"), ("2022-09-27 00:00:00.000", "2022-09-27 02:00:00.000"), ("2022-09-27 02:00:00.000", "2022-09-27 03:00:00.000")]
  #  stringToDatetime(time_list)#works
   # superSort(time_list)
   # print("length of list: ", len(time_list))
    #print("sorted list:")
    #for i in time_list:
    #    print(i[0], " , ", i[1])
    #freeTimeList = removeOverlap(time_list)

    #print sorted and formatted list out 
    #print("doubles removed???")
    #for i in freeTimeList:
    #    print(i)
    #print free time
 #   freeTimeList = freeTimeInDay(freeTimeList)
 #   for i in freeTimeList:
#        print(i)
#if __name__ == "__main__":
#    main()
