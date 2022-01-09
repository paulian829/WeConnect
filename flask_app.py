from datetime import timedelta
from enum import unique
from flask import Flask, render_template, request, json, redirect, url_for, session, send_from_directory, current_app, jsonify, escape
from flask.helpers import make_response
from werkzeug.wrappers import response
from database import *
import os
from datetime import datetime
import random
import http.client
import json


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'
PROFILE_IMAGES = 'static/uploads/ProfilePictures'
# UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROFILE_IMAGES'] = PROFILE_IMAGES

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

@app.after_request
def add_security_headers(resp):
    # resp.headers['Content-Security-Policy']='default-src \'self\''
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.set_cookie('username', 'flask', secure=True, httponly=True, samesite='Lax')
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'


    return resp

@app.route("/", methods=['GET', 'POST'])
def login():
    result = ''
    session['logged_in'] = False
    if request.method == 'POST':
        email = request.form.get('Email')
        print(email)
        password = request.form.get('Password')
        if (len(email) == 0 or len(password) == 0):
            result = "Error"
            return render_template('login.html', result=result)
        result = loginDB(email, password)
        if(result == "Error"):
            return render_template(('login.html'), result = result)

        # session['logged_in'] = True
        session['userID'] = result[0][0]
        session['name'] = result[0][3] + " " + result[0][4]
        session['profilePic'] = result[0][8]
        session['phone'] = result[0][5]
        # session['smsverify'] = random.randint(1000,9999)
        session['smsverify'] = 1235
        # Send to phone number
        # sendMessage()
        if(result[0][6] == 1):
            session['admin'] = True
        else:
            session['admin'] = False
        # return redirect(url_for('dashboard'))
        return render_template(('verify.html'),result='')
        # Direct to the phone verification Screen
    return render_template(('login.html'), result = result)

@app.route("/verify", methods = ['POST','GET'])
def verify():
    if not session['smsverify']:
        return redirect(url_for("forbidden"))
    if request.method == 'POST':
        code = request.form.get("code")
        print(code, session['smsverify'])
        if code == str(session['smsverify']):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('verify.html')

def sendMessage():
    phone = session['phone']
    code = session['smsverify']
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F1dGg6ODA4MC9hcGkvdjEvdXNlcnMvYXBpL2tleS9nZW5lcmF0ZSIsImlhdCI6MTY0MTMwMzIzNSwibmJmIjoxNjQxMzAzMjM1LCJqdGkiOiJvUExDSVJxbk9Mb29YaVBLIiwic3ViIjozMjQ0NjIsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.RNeo7VohKiBBfo1_EyCwFsBPHej9ausI3KVIPe45beo'
    conn = http.client.HTTPSConnection("api.sms.to")
    payload = {
        "message" : "Weconnect OTP code" + str(code), 
        "to" : "+" + str(phone), 
        "sender_id" : "SMSto"
        }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
    }
    conn.request("POST", "/sms/send", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))





@app.route("/register", methods=['GET', 'POST'])
def register():
    positions = getAll("position")
    if request.method == 'POST':
        username = request.form.get("Username")
        email = request.form.get('Email')
        password = request.form.get('Password')
        repeatPass = request.form.get('RepeatPass')
        name = request.form.get('Name')
        phoneNumber = request.form.get('PhoneNumber')
        position = request.form.get('Position')
        print(username)
        result = registerNewUser(
            username, email, password, repeatPass, name, phoneNumber, position)
        print(result)
        return redirect(url_for('admin'))
    else:
        return render_template('register.html', positions=positions)


@app.route("/admin/edit/<id>", methods=['GET', 'POST'])
def viewUser(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    positions = getAll("position")
    result = getUserData(id)
    return render_template("admin-view-profile.html", result=result, positions=positions, title='ADMIN')


@app.route("/forgotpassword")
def forgotpassword():
    return render_template('forgot-password.html')


@app.route("/test")
def test():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    id = session['userID']
    number_of_files_uploaded = getNumberOfFilesUploaded(id)
    number_of_files_passed = getNumberOfFilesPassed(id)
    number_of_files_deadline = getNumberOfFilesDeadline(id)
    number_of_files_nearing_Deadline = getNumberOfFilesNearDeadline(id)
    five_files = getNFiles(id, 5)

    dict = {"number_of_files": number_of_files_uploaded,
            "number_of_files_passed": number_of_files_passed,
            "number_of_files_deadline": number_of_files_deadline,
            "number_of_files_nearing_Deadline": number_of_files_nearing_Deadline,
            "five_files": five_files}

    return json.dumps(dict)


@app.route("/getmyfiles")
def getmyfiles():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    id = session['userID']
    getSixFiles = getNFiles(id, 5)
    getAll = getAllFilesUser(id)

    dict = {"six_files": getSixFiles,
            "getall": getAll
            }
    print(dict)

    return json.dumps(dict)

@app.route('/getUserDetails/<id>')
def getUserDetails(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    user = getUserData(id)
    
    dict = {"userData": user}
    return json.dumps(dict, indent=4, sort_keys=True, default=str)

    # return json.dumps(dict)


@app.route('/getTeachers/')
def getTeachers():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    user = getAllUsers()
    print("+++++++++++++", user)
    dict = {"users": user}
    return json.dumps(dict)



@app.route("/home")
def home():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'HOME'
    items = [
        {"message": 'Foo.pdf', "key": 0},
        {"message": 'Foo.pdf', "key": 1},
        {"message": 'Foo.pdf', "key": 2},
        {"message": 'Foo.pdf', "key": 3},
        {"message": 'Foo.pdf', "key": 4},
        {"message": 'Bar.pdf', "key": 5},
        {"message": 'Bar.pdf', "key": 6},
        {"message": 'Bar.pdf', "key": 7},
        {"message": 'Bar.pdf', "key": 8},
        {"message": 'Bar.pdf', "key": 9},
    ]
    # print(session['userID'])
    # print(session['name'])
    print(session)
    if session['logged_in'] is False:
        return redirect(url_for('login'))

    return render_template("home.html", title=title, name=session['name'], items=items)


@app.route("/uploadProfileImg", methods=['GET', 'POST'])
def uploadProfileImg():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    if request.method == 'POST':
        return "OK you got it"


@app.route("/admin/thrash")
def adminThrash():
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    title = 'ADMIN'
    return render_template("admin-trash.html", title=title)


@app.route("/myfiles")
def myFiles():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    positions = getAll("position")
    title = 'MY FILES'
    return render_template("myFiles.html", title=title, positions=positions)


@app.route("/admin/comments")
def adminComments():
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    title = 'ADMIN'
    return render_template("admin-comments.html", title=title)


@app.route("/admin/password")
def adminPassword():
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    title = 'Password'
    return render_template("admin-password.html", title=title)


@app.route("/dashboard")
# ALSO SAVE AN EVENT IN CASE FOR NOTIFICATIONS
def dashboard():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    positions = getAll("position")
    title = 'DASHBOARD'
    return render_template("dashboard.html", title=title, positions=positions)


@app.route("/pinned")
def pinned():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'PINNED'
    return render_template("pinned.html", title=title)


@app.route("/shared")
def shared():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'SHARED FILES'
    return render_template("shared.html", title=title)


@app.route("/deleted")
def deleted():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'DELETE'
    return render_template("delete.html", title=title)

@app.route('/users')
def users():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'USERS'
    users = getAllUsers()
    return render_template('users.html', title=title,users=users)

@app.route('/schedule/')
def schedule():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'TASKS'
    results = getAllTask()
    id = session['userID']
    return render_template('Schedule.html', title=title,results = results)

@app.route('/schedule/get/<id>')
def getSchedule(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'TASKS'
    results = getOneTask(id)
    id = session['userID']
    return render_template('singletask.html', title=title,results = results,id = id)

@app.route('/updatetask/<status>/<taskID>')
def updateTask(status,taskID):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'TASKS'
    result = updateTaskStatus(status,taskID)
    print(status)
    return redirect(url_for('getSchedule', id=taskID))
    



@app.route('/schedule/add', methods=['GET', 'POST'])
def addSchedule():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    if request.method == 'POST':
        taskName = request.form.get("taskName")
        # imageBlob = request.files['taskImage'].file.name
        deadline = request.form.get("Deadline")
        deadline_datetime = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        print(deadline_datetime)
        schedule = request.form.get("Schedule")
        description = request.form.get('description')
        taskCreatedBy = session['userID']

        result = addTask(taskName,"imageBlob", taskCreatedBy,  deadline_datetime, description, schedule)
        if result:
            return redirect(url_for("schedule"))
        else:
            return 'error'
@app.route('/checkifuseruploaded/<userID>/<taskID>')
def checkifuseruploaded(userID, taskID):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    result = checkIfUserUploadedDB(userID, taskID)
    dict = {"result": result}
    return json.dumps(dict) 

@app.route("/settings")
def settings():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'SETTINGS'
    return render_template("settings.html", title=title)


@app.route("/UpdateUser", methods=['GET', 'POST'])
def updateUser():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    if request.method == "POST":
        id = request.form.get("id")
        requesttype = request.form.get("type") 
        email = request.form.get('Email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phoneNumber = request.form.get('PhoneNumber')
        position = request.form.get('Position')
    result = updateUserDB(id, email, firstName, lastName,
                          phoneNumber, position)
    if result == True and requesttype == 'profile':
        return redirect(url_for("profile"))
    
    if result == True and requesttype == 'admin':
        return redirect(url_for("admin"))


@app.route("/admin/users", methods=['GET', 'POST'])
def admin(result=''):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    title = 'ADMIN'
    positions = getAll("position")
    if request.method == 'POST':
        if(request.form.get("delete")):
            deleteID = request.form.get("delete")
            result = deleteUserDB(deleteID)
            users = getAllUsers()
            return render_template("admin.html", title=title, positions=positions, result=result, users=users)
        email = request.form.get('Email')
        password = request.form.get('Password')
        repeatPass = request.form.get('RepeatPass')
        firstName = request.form.get('FirstName')
        lastName = request.form.get('LastName')
        phoneNumber = request.form.get('PhoneNumber')
        position = request.form.get('Position')
        result = registerNewUser(
            email, password, repeatPass, firstName, lastName, phoneNumber, position)
        users = getAllUsers()
        return render_template("admin.html", title=title, positions=positions, result=result, users=users)

    users = getAllUsers()
    return render_template("admin.html", title=title, positions=positions, result=result, users=users)


@app.route("/admin/files")
def adminFiles():
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    title = 'ADMIN'
    files = getAllFilesForAdmin()
    return render_template("adminFiles.html", title=title,files=files)


@app.route("/profile/")
def profile():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = 'PROFILE'
    # Check if Sessions Exist
    if session['logged_in'] is False:
        return redirect(url_for('login'))

    result = getUserData(session['userID'])
    positions = getAll("position")
    return render_template("profile.html", title=title, result=result, position=positions, positions=positions)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadfile", methods=['GET', 'POST'])
def uploadFile():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = "FILE UPLOAD"
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            filename = request.form.get("filename")
            print(filename)
            # filesize = len(file.read())
            filesize = 1
            filetype = 'block doc'
            file_content_type = 'test'
            share_to_group = request.form.get("Position")
            share_to_user = request.form.get("targetUser")
            deadline = request.form.get('Deadline')
            revision = 1
            uploaded_by = session['userID']
            FilePathName = str(uploaded_by) + filename
            if request.form.get('taskID'):
                taskID = request.form.get('taskID')
            else:
                taskID = 0
            lastID = saveFiletoDb(filename, filetype, filesize, file_content_type,
                                  uploaded_by, share_to_user, share_to_group, deadline, revision,taskID,FilePathName)
            return redirect(url_for('editor', id=lastID[0][0], ))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)

        print(file.filename)
        # filesize
        filename = file.filename
        # filesize = len(file.read())
        filesize = 1
        filetype = 'raw file'
        file_content_type = file.content_type
        share_to_group = 1
        share_to_user = request.form.get("targetUser")
        deadline = request.form.get('Deadline')
        revision = 1
        uploaded_by = session['userID']
        FilePathName = str(uploaded_by) + filename
        if request.form.get('taskID'):
                taskID = request.form.get('taskID')
        else:
                taskID = 0
        lastID = saveFiletoDb(filename, filetype, filesize, file_content_type,
                              uploaded_by, share_to_user, share_to_group, deadline, revision,taskID,FilePathName)

        file.save(os.path.join(app.root_path,
                  app.config['UPLOAD_FOLDER'], FilePathName))
        # print(lastID[0][0])
        if request.form.get('taskID'):
            return redirect(url_for('getSchedule', id=request.form.get('taskID')))
        else:
            return redirect(url_for('file', id=lastID[0][0]))

    return render_template("fileupload.html", title=title)

@app.route('/uploadprofilepic', methods=['GET', 'POST'])
def uploadprofilepic():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    if request.method == 'POST':
        file = request.files['file']
        id = request.form.get('id')
        FilePathName = f"{id}_{file.filename}"
        pathToDb = (f"/{app.config['PROFILE_IMAGES']}/{FilePathName}")
        file.save(os.path.join(app.root_path,
                  app.config['PROFILE_IMAGES'], FilePathName))
        session['profilePic'] = pathToDb
        addProfilePicDB(pathToDb,id)
        return redirect(url_for('profile'))



@app.route('/uploads', methods=['GET', 'POST'])
def download(filename="FILENAME.png"):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads)
    return send_from_directory(uploads, filename)


@app.route('/file/<id>')
def file(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    result = getFileDb(id)
    result = result[0]
    title = "File"
    if result[2] == 'block doc':
        return render_template("editor.html", title=title, result=result)

    # if result[5] != session['userID']:
    #     return redirect(url_for("forbidden"))
    return render_template("file.html", title=title, result=result)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/test123", methods=['GET', 'POST'])
def getEditorData():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    data = request.args.get('data')
    id = int(request.args.get('id'))
    print("DATA", data)
    print("ID", type(id))
    updateDocDB(id, data)

    return 'test'


@app.route("/forbidden")
def forbidden():
    return render_template("forbidden.html")


@app.route("/thrash/<fileid>")
def thrash(fileid):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    result = moveFileToThrash(fileid)
    return redirect(url_for('myFiles'))


@app.route("/editor/<id>")
def editor(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    title = "FILE EDITOR"
    result = getFileDb(id)
    result = result[0]
    print(result)
    return render_template("editor.html", title=title, result=result)


@app.route("/restore/<id>")
def restore(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    result = restoreFileDB(id)
    return redirect(url_for('myFiles'))


@app.route("/emptytrash", methods=['GET', 'POST'])
def emptyTrash():
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    id = session['userID']
    result = emptyTrashDb(id)
    return redirect(url_for("deleted"))


@app.route("/pin/<id>/<status>", methods=['GET', 'POST'])
def setPinned(id, status):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    result = setStatusPinned(id, status)
    print('success')
    return redirect(url_for('file', id=id))

@app.route('/admin/deleteuser/<id>')
def deleteUser(id):
    
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    result = deleteUserDB(id)
    return redirect(url_for('admin'))

@app.route('/admin/deletefile/<id>')
def deletefile(id):
    
    if session['admin'] == False:
        return redirect(url_for("forbidden"))
    result = deleteFileDB(id)
    return redirect(url_for('adminFiles'))

@app.route('/task/delete/<id>')
def deletefileTask(id):
    if not session['logged_in']:
        return redirect(url_for("forbidden"))
    result = deleteFileDB(id)
    return redirect(url_for('schedule'))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


# https://www.youtube.com/watch?v=71EU8gnZqZQ
