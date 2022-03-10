from collections import UserList
from datetime import time, timedelta
from enum import unique
from getpass import getpass
from flask import (
    Flask,
    render_template,
    request,
    json,
    redirect,
    url_for,
    session,
    send_from_directory,
    current_app,
    jsonify,
    escape,
)
import time
from flask.helpers import make_response
from werkzeug.wrappers import response
from database import *
import os
from datetime import datetime
import random
import http.client
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = "static/uploads"
PROFILE_IMAGES = "static/uploads/ProfilePictures"
# UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.secret_key = "super secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROFILE_IMAGES"] = PROFILE_IMAGES

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


@app.after_request
def add_security_headers(resp):
    # resp.headers['Content-Security-Policy']='default-src \'self\''
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.set_cookie("username", "flask", secure=True,
                    httponly=True, samesite="Lax")
    resp.headers["X-XSS-Protection"] = "1; mode=block"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    return resp


@app.route("/", methods=["GET", "POST"])
def login():
    result = ""
    session["logged_in"] = False
    if request.method == "POST":
        email = request.form.get("Email")
        print(email)
        password = request.form.get("Password")
        if len(email) == 0 or len(password) == 0:
            result = "Error"
            return render_template("login.html", result=result)
        result = loginDB(email, password)
        if result == "Error":
            return render_template(("login.html"), result=result)

        # session['logged_in'] = True
        session["userID"] = result[0][0]
        session["name"] = result[0][3] + " " + result[0][4]
        session["email"] = result[0][1]
        session["profilePic"] = result[0][8]
        session["phone"] = result[0][5]
        # session['smsverify'] = random.randint(1000,9999)
        session["smsverify"] = 1235
        session['position'] = result[0][6]
        # Send to phone number
        # sendMessage()
        if result[0][6] == 1:
            session["admin"] = True
        else:
            session["admin"] = False
        # return redirect(url_for('dashboard'))
        return render_template(("verify.html"), result="")
        # Direct to the phone verification Screen
    return render_template(("login.html"), result=result)


@app.route("/verify", methods=["POST", "GET"])
def verify():
    if not session["smsverify"]:
        return redirect(url_for("forbidden"))
    if request.method == "POST":
        code = request.form.get("code")
        print(code, session["smsverify"])

        if code == str(session["smsverify"]):
            session["logged_in"] = True
            if session["admin"] == True:
                return redirect(url_for("admin"))

            return redirect(url_for("dashboard"))
    return render_template("verify.html", result='')


def sendMessage():
    "SMS.to"
    phone = session["phone"]
    code = session["smsverify"]
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F1dGg6ODA4MC9hcGkvdjEvdXNlcnMvYXBpL2tleS9nZW5lcmF0ZSIsImlhdCI6MTY0MTMwMzIzNSwibmJmIjoxNjQxMzAzMjM1LCJqdGkiOiJvUExDSVJxbk9Mb29YaVBLIiwic3ViIjozMjQ0NjIsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.RNeo7VohKiBBfo1_EyCwFsBPHej9ausI3KVIPe45beo"
    conn = http.client.HTTPSConnection("api.sms.to")
    payload = {
        "message": "Weconnect OTP code" + str(code),
        "to": "+" + str(phone),
        "sender_id": "SMSto",
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + api_key}
    conn.request("POST", "/sms/send", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


@app.route("/register", methods=["GET", "POST"])
def register():
    positions = getAll("position")
    if request.method == "POST":
        username = request.form.get("Username")
        email = request.form.get("Email")
        password = request.form.get("Password")
        repeatPass = request.form.get("RepeatPass")
        name = request.form.get("Name")
        phoneNumber = request.form.get("PhoneNumber")
        position = request.form.get("Position")
        print(username)
        result = registerNewUser(
            username, email, password, repeatPass, name, phoneNumber, position
        )
        print(result)
        return redirect(url_for("admin"))
    else:
        return render_template("register.html", positions=positions)


@app.route("/admin/edit/<id>", methods=["GET", "POST"])
def viewUser(id):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    positions = getAll("position")
    result = getUserData(id)
    if result:
        return render_template(
            "admin-view-profile.html", result=result, positions=positions, title="ADMIN"
        )
    else:
        return render_template("404.html")


@app.route("/forgotpassword")
def forgotpassword():
    result = ""
    if request.args.get("result"):
        result = request.args.get("result")
    print(result)
    return render_template("forgot-password.html", result=result)


@app.route("/resetpassword", methods=["POST"])
def reset():
    if request.method == "POST":
        email = request.form.get("Email")
        print(email)
        sender_address = "weconnect.thesis@gmail.com"
        sender_pass = "eplnssqbajzfqonw"
        # Setup the MIME
        # Check 1st if user Exist
        result = getUserViaEmail(email)
        if len((result)) == 0:
            print("error")
            return redirect(url_for("forgotpassword", result="Error"))
        userID = result[0][0]  # ignore ERrors
        print(userID)

        # get the User ID

        content = f"Reset password link: {request.base_url}/{userID}"
        print(content)
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = email
        message["Subject"] = "Password Reset"  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(content, "plain"))
        # Create SMTP session for sending the mail
        sessionEmail = smtplib.SMTP(
            "smtp.gmail.com", 587)  # use gmail with port
        sessionEmail.starttls()  # enable security
        sessionEmail.login(
            sender_address, sender_pass
        )  # login with mail_id and password
        text = message.as_string()
        sessionEmail.sendmail(sender_address, email, text)
        sessionEmail.quit()
        session["resetPassword"] = email
        print("Mail Sent")
        return redirect(url_for("forgotpassword", result="Success"))


@app.route("/resetpassword/<id>")
def resetPass(id):
    user = getUserData(id)
    print(user[0][1])
    if session["resetPassword"] != user[0][1]:
        return redirect(url_for("forbidden"))
    result = ""
    if request.args.get("result"):
        result = request.args.get("result")

    return render_template("reset.html", id=id, result=result)


@app.route("/resetpassword/<id>/update", methods=['POST'])
def submitResetPass(id):
    user = getUserData(id)
    result = ''
    print(user[0][1])
    if session["resetPassword"] != user[0][1]:
        return redirect(url_for("forbidden"))

    if request.method == "POST":
        password = request.form.get("pass")
        rePass = request.form.get("Repass")
        if password != rePass:
            return redirect(url_for("resetPass", result="Error", id=id))
        result = resetPassword(password, id)
        return redirect(url_for("login"))

    return redirect(url_for("resetPass", id=id, result=result))


@app.route("/test")
def test():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    id = session["userID"]
    email = session['email']
    number_of_files_uploaded = 0
    if session['position'] == 4:
        number_of_files_uploaded = getNumberOfFilesUploaded(id)
        number_of_files_passed = getNumberOfFilesPassed(id)
        number_of_files_deadline = len(getPendingTeachersList(id, 'failed'))
        number_of_files_nearing_Deadline = getNumberOfFilesNearDeadline(id)

    elif session['position'] == 3:
        number_of_files_uploaded = getNumberOfFilesUploaded(id)
        number_of_files_passed = getPassed('Pending Grade Chairman', False)
        number_of_files_deadline = getFailed('Pending Teachers', False)
        number_of_files_nearing_Deadline = getPending(
            'Pending Teachers', False)

    elif session['position'] == 5:
        number_of_files_uploaded = getNumberOfFilesUploaded(id)
        number_of_files_passed = getPassed('Pending Principal', False)
        number_of_files_deadline = getFailed('Pending Principal', False)
        number_of_files_nearing_Deadline = getPending(
            'Pending Principal', False)

    elif session['position'] == 2:
        number_of_files_uploaded = getNumberOfFilesUploaded(id)
        number_of_files_passed = getPassed(
            'Pending District Supervisor', False)
        number_of_files_deadline = getFailed(
            'Pending District Supervisor', False)
        number_of_files_nearing_Deadline = getPending(
            'Pending District Supervisor', False)

    five_files = getNFiles(id, 5, email)
    dict = {
        "number_of_files": number_of_files_uploaded,
        "number_of_files_passed": number_of_files_passed,
        "number_of_files_deadline": number_of_files_deadline,
        "number_of_files_nearing_Deadline": number_of_files_nearing_Deadline,
        "five_files": five_files,
    }

    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route("/getmyfiles")
def getmyfiles():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    id = session["userID"]
    email = session['email']
    getSixFiles = getNFiles(id, 5, email)
    sort = request.args.get('sort')
    getAll = getAllFilesUser(id, email, sort)
    print(getAll)
    dict = {"six_files": getSixFiles, "getall": getAll}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route("/getUserDetails/<id>")
def getUserDetails(id):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    user = getUserData(id)

    dict = {"userData": user}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)

    # return json.dumps(dict)


@app.route("/getTeachers/")
def getTeachers():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    user = getAllUsers()
    dict = {"users": user}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route("/home")
def home():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "HOME"
    items = [
        {"message": "Foo.pdf", "key": 0},
        {"message": "Foo.pdf", "key": 1},
        {"message": "Foo.pdf", "key": 2},
        {"message": "Foo.pdf", "key": 3},
        {"message": "Foo.pdf", "key": 4},
        {"message": "Bar.pdf", "key": 5},
        {"message": "Bar.pdf", "key": 6},
        {"message": "Bar.pdf", "key": 7},
        {"message": "Bar.pdf", "key": 8},
        {"message": "Bar.pdf", "key": 9},
    ]
    # print(session['userID'])
    # print(session['name'])
    print(session)
    if session["logged_in"] is False:
        return redirect(url_for("login"))

    return render_template("home.html", title=title, name=session["name"], items=items)


@app.route("/uploadProfileImg", methods=["GET", "POST"])
def uploadProfileImg():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    if request.method == "POST":
        return "OK you got it"


@app.route("/admin/thrash")
def adminThrash():
    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    title = "ADMIN"
    return render_template("admin-trash.html", title=title)


@app.route("/myfiles")
def myFiles():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    positions = getAll("position")
    title = "MY FILES"
    return render_template("myFiles.html", title=title, positions=positions, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route("/admin/comments")
def adminComments():
    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    title = "ADMIN"
    results = getAllComments()
    users = getAllUsers()
    return render_template("admin-comments.html", title=title, results=results, users=users)


@app.route("/admin/password")
def adminPassword():
    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    title = "Password"
    return render_template("admin-password.html", title=title)


@app.route("/dashboard")
def dashboard():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))

    positions = getAll("position")
    title = "DASHBOARD"
    checkIfHaveNotifications()
    return render_template("dashboard.html", title=title, positions=positions, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


def checkIfHaveNotifications():
    UserList = getEventFromDB1()
    print(UserList)
    unseen = 0
    for events in UserList:
        if events[1] != session['userID']:
            if events[-1] == 0:
                unseen = unseen + 1
    eventsDB = getEvent(session["userID"])
    for event in eventsDB:
        if event[1] == session['userID']:
            if event[6] == 'Task':
                if event[5] == 0:
                    unseen = unseen + 1

    return unseen


def getEventFromDB1():
    events = getEvent(session["userID"])
    UserList = list()
    for event in events:
        userIDresult = getUserData(event[1])
        if userIDresult:
            print(userIDresult)
            for userDetails in userIDresult:
                name = userDetails[3] + " " + userDetails[4]
                id = userDetails[0]
                email = userDetails[1]
                profilepic = userDetails[8]
                seen = event[5]

                uploaderDetails = (1, id, name, email, profilepic, seen)
                UserList.append(uploaderDetails)
    UserList = list(dict.fromkeys(UserList))

    return UserList


def getEventFromDB():
    events = getEvent(session["userID"])
    UserList = list()
    for event in events:
        userIDresult = getUserData(event[1])
        if userIDresult:
            for userDetails in userIDresult:
                name = userDetails[3] + " " + userDetails[4]
                id = userDetails[0]
                email = userDetails[1]
                profilepic = userDetails[8]
                seen = event[5]
                eventID = event[0]
                eventUploader = event[1]
                eventFileID = event[2]
                eventDateUploaded = event[3]
                eventTarget = event[4]
                eventType = event[6]

                uploaderDetails = (1, id, name, email, profilepic, seen, eventID,
                                   eventUploader, eventFileID, eventDateUploaded, eventTarget, eventType)
                UserList.append(uploaderDetails)

    # UserList = list(dict.fromkeys(UserList))
    print("USERS", UserList)
    return UserList


@app.route("/pinned")
def pinned():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "PINNED"
    return render_template("pinned.html", title=title, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route("/shared")
def shared():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "SHARED FILES"
    return render_template("shared.html", title=title)


@app.route("/deleted")
def deleted():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "DELETE"
    return render_template("delete.html", title=title, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route("/users")
def users():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "USERS"
    users = getAllUsers()
    return render_template("users.html", title=title, users=users, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route("/schedule/")
def schedule():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "TASKS"
    results = getAllTask()
    userID = session['userID']
    status_list = list()
    today = datetime.today()
    print(today)
    if session['position'] == 4:
        for result in results:
            print((result[5]))
            Match = getMatch(userID, result[0])
            if Match:
                status = (result[0], "Done")
            elif today > result[5]:
                status = (result[0], 'Failed Deadline')
            else:
                print(result[7])
                if result[7] != 'Pending Teachers':
                    print('Failed')
                    status = (result[0], 'Pending')
                else:
                    print('Pending')
                    status = (result[0], 'Pending')
            status_list.append(status)
    if session['position'] == 3:
        for result in results:
            print('***********************')
            print(result[7])
            if result[7] == "Pending Teachers":
                if result[5] < today:
                    status = (result[0], 'Failed Deadline')
                else:
                    status = (result[0], 'Pending')
            elif result[7] == "Pending Grade Chairman":
                if result[5] < today:
                    status = (result[0], 'Failed Deadline')
                else:
                    status = (result[0], 'Pending')
            elif result[7] == "Pending Principal" or result[7] == "Pending District Supervisor" or result[7] == 'Done':
                status = (result[0], "Done")
            else:
                status = (result[0], "Pending")
            status_list.append(status)

    if session['position'] == 5:
        for result in results:
            if result[7] == 'Pending Principal':
                if result[5] < today:
                    status = (result[0], 'Failed Deadline')
                else:
                    status = (result[0], 'Pending')
            elif result[7] == 'Pending Teachers' or result[7] == 'Pending Grade Chairman':
                if result[5] < today:
                    status = (result[0], 'Failed Deadline')
                else:
                    status = (result[0], 'Waiting')
            elif result[7] == 'Pending District Supervisor' or result[7] == 'Done':
                status = (result[0], 'Done')
            else:
                status = (result[0], 'Pending')
            status_list.append(status)
    if session['position'] == 2:
        for result in results:
            if result[7] == 'Pending District Supervisor':
                if result[5] < today:
                    status = (result[0], 'Failed Deadline')
                else:
                    status = (result[0], 'Pending')
            elif result[7] == 'Done':
                status = (result[0], 'Done')
            elif result[7] == 'Pending Teachers' or result[7] == 'Pending Grade Chairman' or result[7] == 'Pending Principal':
                if result[5] < today:
                    status = (result[0], 'Failed Deadline')
                else:
                    status = (result[0], 'Waiting')

            else:
                status = (result[0], 'Pending')
            status_list.append(status)

    print(status_list)
    return render_template("Schedule.html", title=title, results=results, status_list=status_list, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route("/schedule/get/<id>")
def getSchedule(id):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))

    notif = request.args.get("notif")
    if notif:
        print("PLEASE UNSEE")
        result = checkEvent(notif)

    title = "TASKS"
    results = getOneTask(id)
    id = session["userID"]
    return render_template("singletask.html", title=title, results=results, id=id, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route('/admin/tasks/<sched>')
def getTasks(sched):
    # if not session["admin"]:
    #     return redirect(url_for("forbidden"))
    results = getTasksDB(sched)
    return render_template("singletaskadmin.html", title='ADMIN', results=results)


@app.route('/admin/tasks/edit/<id>')
def getTaskForEdit(id):
    # if not session["admin"]:
    #     return redirect(url_for("forbidden"))
    result = getOneTask(id)
    dict = {"result": result}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route("/updatetask/<status>/<taskID>")
def updateTask(status, taskID):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "TASKS"
    today = datetime.today()
    result = updateTaskStatus(status, taskID)
    print(status)
    if (status == 'Pending Principal'):
        principals = get_User_view_position(5)
        for user in principals:
            createEvent(session['userID'],taskID,today,user[0],'Task Forward')
    if (status == 'Pending District Supervisor'):
        users = get_User_view_position(2)
        for user in users:
            createEvent(session['userID'],taskID,today,user[0],'Task Forward')

    print(status)
    return redirect(url_for("getSchedule", id=taskID))


@app.route("/schedule/add", methods=["GET", "POST"])
def addSchedule():
    if request.method == "POST":
        taskName = request.form.get("taskName")
        # imageBlob = request.files['taskImage'].file.name
        deadline = request.form.get("Deadline")
        deadline_datetime = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        print(deadline_datetime)
        schedule = request.form.get("Schedule")
        description = request.form.get("description")
        taskCreatedBy = session["userID"]

        result = addTask(
            taskName,
            "imageBlob",
            taskCreatedBy,
            deadline_datetime,
            description,
            schedule,
        )
        if result:
            today = datetime.today()
            teachers = get_User_view_position(4)
            for teacher in teachers:
                lastTask = get_last_task()
                createEvent(taskCreatedBy,
                            lastTask[0], today, teacher[0], 'New Task')
            return redirect(url_for("schedule"))
        else:
            return "error"


@app.route("/schedule/edit", methods=["POST"])
def editSchedule():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    if request.method == "POST":
        taskID = request.form.get('taskID')
        print("Task ID", taskID)
        taskName = request.form.get("taskName")
        # imageBlob = request.files['taskImage'].file.name
        deadline = request.form.get("Deadline")
        deadline_datetime = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        print(deadline_datetime)
        schedule = request.form.get("Schedule")
        description = request.form.get("description")
        taskCreatedBy = session["userID"]
        status = request.form.get('Status')
        result = updateTaskDB(taskID, taskName, "imageBlob", taskCreatedBy,
                              deadline_datetime, description, schedule, status)
        if result:
            if session['admin']:
                return redirect(url_for("getTasks", sched='Weekly'))
            else:
                return redirect(url_for("schedule"))
        else:
            return "error"


@app.route("/checkifuseruploaded/<userID>/<taskID>")
def checkifuseruploaded(userID, taskID):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    result = checkIfUserUploadedDB(userID, taskID)
    dict = {"result": result}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route('/admin/deleteTask/<id>')
def deleteTask(id):
    result = deleteTaskDb(id)
    return redirect(url_for("schedule"))


@app.route("/settings")
def settings():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "SETTINGS"
    return render_template("settings.html", title=title)


@app.route("/UpdateUser", methods=["GET", "POST"])
def updateUser():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    if request.method == "POST":
        id = request.form.get("id")
        requesttype = request.form.get("type")
        email = request.form.get("Email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        phoneNumber = request.form.get("PhoneNumber")
        position = request.form.get("Position")
    result = updateUserDB(id, email, firstName, lastName,
                          phoneNumber, position)
    if result == True and requesttype == "profile":
        return redirect(url_for("profile"))

    if result == True and requesttype == "admin":
        return redirect(url_for("admin"))


@app.route("/admin/users", methods=["GET", "POST"])
def admin(result=""):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    title = "ADMIN"
    positions = getAll("position")
    if request.method == "POST":
        if request.form.get("delete"):
            deleteID = request.form.get("delete")
            result = deleteUserDB(deleteID)
            users = getAllUsers()
            return render_template(
                "admin.html",
                title=title,
                positions=positions,
                result=result,
                users=users,
            )
        email = request.form.get("Email")
        if '.' not in email:
            print("Found!")
            users = getAllUsers()
            result = "email error"
            return render_template(
                "admin.html", title=title, positions=positions, result=result, users=users
            )
        password = request.form.get("Password")
        repeatPass = request.form.get("RepeatPass")
        firstName = request.form.get("FirstName")
        lastName = request.form.get("LastName")
        phoneNumber = str(request.form.get("PhoneNumber"))
        if len(phoneNumber) < 10:
            users = getAllUsers()
            result = "phone error"
            return render_template(
                "admin.html", title=title, positions=positions, result=result, users=users
            )
        phoneNumber = "+63" + phoneNumber
        position = request.form.get("Position")
        result = registerNewUser(
            email, password, repeatPass, firstName, lastName, phoneNumber, position
        )
        users = getAllUsers()
        return render_template(
            "admin.html", title=title, positions=positions, result=result, users=users
        )

    users = getAllUsers()
    return render_template(
        "admin.html", title=title, positions=positions, result=result, users=users
    )


@app.route("/admin/files")
def adminFiles():
    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    title = "ADMIN"
    if request.args.get("sort"):
        sort = request.args.get("sort")
        files = getAllFilesForAdminSorted(sort)
        return render_template("adminFiles.html", title=title, files=files)
    files = getAllFilesForAdmin()
    return render_template("adminFiles.html", title=title, files=files)


@app.route("/profile/")
def profile():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "PROFILE"
    # Check if Sessions Exist
    if session["logged_in"] is False:
        return redirect(url_for("login"))

    result = getUserData(session["userID"])
    positions = getAll("position")
    return render_template(
        "profile.html",
        title=title,
        result=result,
        position=positions,
        positions=positions, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications()
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def sendEmail(receiver_email, sender_ID):
    print(receiver_email)
    sender_address = "weconnect.thesis@gmail.com"
    sender_pass = "eplnssqbajzfqonw"
    # Setup the MIME
    # Check 1st if user Exist
    result = getUserData(sender_ID)
    if len((result)) == 0:
        print("error")
        return redirect(url_for("forgotpassword", result="Error"))
    userID = result[0][1]  # ignore ERrors
    print("UserID", userID)

    # get the User ID

    content = f"User {userID} had Tagged you in file check it now at www.weconnect.sbs"
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_email
    message["Subject"] = "File Tagged"  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(content, "plain"))
    # Create SMTP session for sending the mail
    sessionEmail = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
    sessionEmail.starttls()  # enable security
    sessionEmail.login(
        sender_address, sender_pass
    )  # login with mail_id and password
    text = message.as_string()
    sessionEmail.sendmail(sender_address, receiver_email, text)
    sessionEmail.quit()
    print("Mail Sent")


@app.route("/uploadfile", methods=["GET", "POST"])
def uploadFile():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "FILE UPLOAD"
    if request.method == "POST":
        if "file" not in request.files:
            print("No file part")
            filename = request.form.get("filename")
            print(filename)
            # filesize = len(file.read())
            filesize = 1
            filetype = "block doc"
            file_content_type = "test"
            share_to_group = request.form.get("Position")
            share_to_user = request.form.get("targetUser")
            uploaded_by = session["userID"]
            if request.form.get("targetUser"):
                if share_to_user != "None":
                    print('++++++++++++++')
                    sendEmail(share_to_user, uploaded_by)
            deadline = request.form.get("Deadline")
            revision = 1
            FilePathName = str(uploaded_by) + filename
            if request.form.get("taskID"):
                taskID = request.form.get("taskID")
            else:
                taskID = 0
            lastID = saveFiletoDb(
                filename,
                filetype,
                filesize,
                file_content_type,
                uploaded_by,
                share_to_user,
                share_to_group,
                deadline,
                revision,
                taskID,
                FilePathName,
            )
            return redirect(
                url_for(
                    "editor",
                    id=lastID[0][0],
                )
            )
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return redirect(request.url)

        print(file.filename)
        # filesize
        filename = file.filename
        # filesize = len(file.read())
        filesize = 1
        filetype = filename.split(".")[-1]
        file_content_type = file.content_type
        share_to_group = 1
        uploaded_by = session["userID"]
        share_to_user = request.form.get("targetUser")
        if request.form.get("targetUser"):
            if share_to_user != "None":
                print('++++++++++++++')
                sendEmail(share_to_user, uploaded_by)
        deadline = request.form.get("Deadline")
        revision = 1
        FilePathName = str(uploaded_by) + filename
        today = datetime.today()
        if request.form.get("taskID"):
            taskID = request.form.get("taskID")
            users = get_User_view_position(5)
            for user in users:
                print("test 123 ", user)
                createEvent(session['userID'], taskID,
                            today, user[0], 'Task Upload')
            users = get_User_view_position(3)
            for user in users:
                print("test 123 ", user)
                createEvent(session['userID'], taskID,
                            today, user[0], 'Task Upload')

        else:
            taskID = 0
        lastID = saveFiletoDb(
            filename,
            filetype,
            filesize,
            file_content_type,
            uploaded_by,
            share_to_user,
            share_to_group,
            deadline,
            revision,
            taskID,
            FilePathName,
        )

        file.save(
            os.path.join(
                app.root_path, app.config["UPLOAD_FOLDER"], FilePathName)
        )
        # print(lastID[0][0])
        if request.form.get("taskID"):
            return redirect(url_for("getSchedule", id=request.form.get("taskID")))
        else:
            return redirect(url_for("file", id=lastID[0][0]))

    return render_template("fileupload.html", title=title)


@app.route("/uploadprofilepic", methods=["GET", "POST"])
def uploadprofilepic():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    if request.method == "POST":
        file = request.files["file"]
        id = request.form.get("id")
        FilePathName = f"{id}_{file.filename}"
        pathToDb = f"/{app.config['PROFILE_IMAGES']}/{FilePathName}"
        file.save(
            os.path.join(
                app.root_path, app.config["PROFILE_IMAGES"], FilePathName)
        )
        session["profilePic"] = pathToDb
        addProfilePicDB(pathToDb, id)
        return redirect(url_for("profile"))


@app.route("/uploads", methods=["GET", "POST"])
def download(filename="FILENAME.png"):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    uploads = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
    print(uploads)
    return send_from_directory(uploads, filename)


@app.route("/file/<id>")
def file(id):
    if not session["logged_in"]:
        return redirect(url_for("unsee"))

    notif = request.args.get("notif")
    if notif:
        print("PLEASE UNSEE")
        result = checkEvent(notif)

    result = getFileDb(id)
    print('test result', result)
    if result:
        title = "File"
        deadline = None
        if result[0][14] > 0:
            task = getOneTask(result[0][14])
            if task:
                deadline = task[0][5]

        user = getUserData(result[0][5])
        userName = None
        if user:
            user = user[0]
            userName = user[3] + ' ' + user[4]

        result = result[0]
        return render_template("file.html", title=title, result=result, deadline=deadline, userName=userName, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())
    else:
        title = "File"
        return render_template("file-not-found.html", title=title, result=[], deadline=[], userName=[], events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/test123", methods=["GET", "POST"])
def getEditorData():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    data = request.args.get("data")
    id = int(request.args.get("id"))
    print("DATA", data)
    print("ID", type(id))
    updateDocDB(id, data)

    return "test"


@app.route("/forbidden")
def forbidden():
    return render_template("forbidden.html")


@app.route("/thrash/<fileid>")
def thrash(fileid):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    result = moveFileToThrash(fileid)
    return redirect(url_for("myFiles"))


@app.route("/editor/<id>")
def editor(id):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    title = "FILE EDITOR"
    result = getFileDb(id)
    result = result[0]
    print(result)
    return render_template("editor.html", title=title, result=result)


@app.route("/restore/<id>")
def restore(id):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    result = restoreFileDB(id)
    return redirect(url_for("myFiles"))


@app.route("/emptytrash", methods=["GET", "POST"])
def emptyTrash():
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    id = session["userID"]
    result = emptyTrashDb(id)
    return redirect(url_for("deleted"))


@app.route("/pin/<id>/<status>", methods=["GET", "POST"])
def setPinned(id, status):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    result = setStatusPinned(id, status)
    print("success")
    return redirect(url_for("file", id=id))


@app.route("/admin/deleteuser/<id>")
def deleteUser(id):

    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    result = deleteUserDB(id)
    return redirect(url_for("admin"))


@app.route("/admin/deletefile/<id>")
def deletefile(id):

    if session["admin"] == False:
        return redirect(url_for("forbidden"))
    result = deleteFileDB(id)
    return redirect(url_for("adminFiles"))


@app.route("/task/delete/<id>")
def deletefileTask(id):
    if not session["logged_in"]:
        return redirect(url_for("forbidden"))
    result = deleteFileDB(id)
    return redirect(url_for("schedule"))


@app.route('/comment/new/<userID>/<fileID>/<comment>')
def addComment(userID, fileID, comment):
    Timetoday = time.time()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Timetoday)))
    result = newComment(userID, fileID, comment, Timetoday)
    # Get list of username
    # get commenter
    list_of_users = get_list_of_users(fileID)
    list_of_users.append(get_owner_of_file(fileID))
    list_of_users.append(get_tagged_user(fileID))
    list_of_users = list(dict.fromkeys(list_of_users))
    print(list_of_users)
    today = datetime.today()
    for users in list_of_users:
        if users is not None:
            createEvent(userID, fileID, today, users, "Comment")
    dictOne = {"result": 'result'}
    return json.dumps(dictOne, indent=4, sort_keys=True, default=str)


@app.route('/comments/<fileID>')
def getComments(fileID):
    result = getCommentsDB(fileID)
    dict = {'data': result}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route('/comment/delete/<commentID>')
def deleteComment(commentID):
    result = deleteCommentDB(commentID)
    dict = {'data': result}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)


@app.route('/finished')
def finished():
    title = "Finished Tasks"
    position = session['position']
    userID = session['userID']
    result = ''
    status_list = list()
    today = datetime.today()
    if position == 4:
        results = getNumberOfFilesPassedList(userID)
        for result in results:
            print((result[5]))
            Match = getMatch(userID, result[0])
            if Match:
                status = (result[0], "Done")
            elif today > result[5]:
                status = (result[0], 'Passed Deadline')
            else:
                status = (result[0], 'Pending')
            status_list.append(status)
        print("RESULTS", result)
    if position == 3:
        results = getPassed("Pending Grade Chairman", True)
        for result in results:
            status = (result[0], "Done")
            status_list.append(status)
    if position == 5:
        results = getPassed("Pending Principal", True)
        for result in results:
            status = (result[0], 'Done')
            status_list.append(status)

    if position == 2:
        results = getPassed("Pending District Supervisor", True)
        for result in results:
            status = (result[0], 'Done')
            status_list.append(status)
    return render_template("dashboard-status.html", title=title, results=results, status_list=status_list, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route('/pending')
def pending():
    title = "Pending Tasks"
    position = session['position']
    userID = session['userID']
    results = ''
    status_list = list()
    today = datetime.today()
    if position == 4:
        results = getPendingTeachersList(userID, 'pending')
        print(results)
        for result in results:
            print((result[5]))
            Match = getMatch(userID, result[0])
            if Match:
                status = (result[0], "Done")
            elif today > result[5]:
                status = (result[0], 'Passed Deadline')
            else:
                status = (result[0], 'Pending')
            status_list.append(status)
    if position == 3:
        results = getPending('Pending Teachers', True)
        for result in results:
            status = (result[0], 'Pending')
            status_list.append(status)
    if position == 5:
        results = getPending('Pending Principal', True)
        for result in results:
            status = (result[0], 'Pending')
            status_list.append(status)

    if position == 2:
        results = getPending('Pending District Supervisor', True)
        for result in results:
            status = (result[0], 'Pending')
            status_list.append(status)
    return render_template("dashboard-status.html", title=title, results=results, status_list=status_list, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())


@app.route('/failed')
def failed():
    title = "Failed Tasks"
    position = session['position']
    userID = session['userID']
    results = ''
    status_list = list()
    today = datetime.today()
    if position == 4:
        results = getPendingTeachersList(userID, 'failed')
        print("RESULT", len(results))
        for result in results:
            print((result[5]))
            Match = getMatch(userID, result[0])
            if Match:
                status = (result[0], "Done")
            elif today > result[5]:
                status = (result[0], 'Passed Deadline')
            else:
                status = (result[0], 'Pending')
            status_list.append(status)
    if position == 3:
        results = getFailed('Pending Teachers', True)
        for result in results:
            status = (result[0], 'Passed Deadline')
            status_list.append(status)

    if position == 5:
        results = getFailed("Pending Principal", True)
        for result in results:
            status = (result[0], 'Passed Deadline')
            status_list.append(status)
    if position == 2:
        results = getFailed('Pending District Supervisor', True)
        for result in results:
            status = (result[0], 'Passed Deadline')
            status_list.append(status)
    return render_template("dashboard-status.html", title=title, results=results, status_list=status_list, events=getEvent(session["userID"]), UserList=getEventFromDB(), notif=checkIfHaveNotifications())



@app.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


# https://www.youtube.com/watch?v=71EU8gnZqZQ
