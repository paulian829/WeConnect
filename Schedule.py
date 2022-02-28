from database import *
from datetime import datetime,timedelta
from flask_app import *


def check_scheduled_tasks():
    #Get list of Tasks
    #Check Deadline
    #Set Events to Target Users depending on the tasks status
    list_of_tasks = getAllTask()
    today = datetime.today()

    for tasks in list_of_tasks:
        time_diff = tasks[5] - today 
        time_diff = time_diff / timedelta(minutes=1)
        if time_diff < 1440 and time_diff > 0:
            if tasks[7] == "Pending Teachers":
                results = get_User_view_position(4)
            elif tasks[7] == "Pending Grade Chairman":
                results = get_User_view_position(3)
            elif tasks[7] == "Pending Principal":
                results = get_User_view_position(5)
            elif tasks[7] == "Pending District Supervisor":
                results = get_User_view_position(2)
            else:
                #Do nothing
                print(None)
            for users in results:
                createEvent(users[0],tasks[0],today,users[0],"Task")
            print(results)

check_scheduled_tasks()