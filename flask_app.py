from enum import unique
from flask import Flask, render_template,request,json,redirect,url_for,session,send_from_directory,current_app,jsonify
from database import *
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'
# UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/",methods=['GET','POST'])
def login():
    result = ''
    session['logged_in'] = False
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        if (len(email) == 0 or len(password) == 0 ):
            result = "Error"
            return render_template('login.html',result = result)
        result = loginDB(email, password)
        if(result == "Error"):
            return render_template('login.html',result = result)

        session['logged_in'] = True
        session['userID'] = result[0][0]
        session['name'] = result[0][3] + " " + result[0][4]
        return redirect(url_for('dashboard'))
    return render_template('login.html',result = result)


@app.route("/register", methods=['GET','POST'])
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
        result = registerNewUser(username, email, password, repeatPass, name, phoneNumber, position)
        print(result)
        return redirect(url_for('admin'))
    else:
        return render_template('register.html',positions = positions)

@app.route("/admin/edit/<id>", methods=['GET','POST'])
def viewUser(id):
    positions = getAll("position")
    result = getUserData(id)
    return render_template("admin-view-profile.html", result = result ,positions = positions, title='ADMIN')


@app.route("/forgotpassword")
def forgotpassword():
    return render_template('forgot-password.html')

@app.route("/test")
def test():
    id = session['userID']
    number_of_files_uploaded = getNumberOfFilesUploaded(id)
    number_of_files_passed = getNumberOfFilesPassed(id)
    number_of_files_deadline = getNumberOfFilesDeadline(id)
    number_of_files_nearing_Deadline = getNumberOfFilesNearDeadline(id)
    five_files = getNFiles(id,5)

    dict={"number_of_files":number_of_files_uploaded,
        "number_of_files_passed":number_of_files_passed,
        "number_of_files_deadline":number_of_files_deadline,
        "number_of_files_nearing_Deadline":number_of_files_nearing_Deadline,
        "five_files":five_files}

    return json.dumps(dict)

@app.route("/getmyfiles")
def getmyfiles():
    id = session['userID']
    getSixFiles = getNFiles(id, 6)
    getAll = getAllFilesUser(id)

    dict = {"six_files": getSixFiles,
            "getall":getAll
    }
    print(dict)

    return json.dumps(dict)




@app.route("/home")
def home():
    title = 'HOME'
    items = [
            { "message": 'Foo.pdf', "key": 0 },
            { "message": 'Foo.pdf', "key": 1 },
            { "message": 'Foo.pdf', "key": 2 },
            { "message": 'Foo.pdf', "key": 3 },
            { "message": 'Foo.pdf', "key": 4 },
            { "message": 'Bar.pdf', "key": 5 },
            { "message": 'Bar.pdf', "key": 6 },
            { "message": 'Bar.pdf', "key": 7 },
            { "message": 'Bar.pdf', "key": 8 },
            { "message": 'Bar.pdf', "key": 9 },
        ]
    # print(session['userID'])
    # print(session['name'])
    print(session)
    if session['logged_in'] is False:
        return redirect(url_for('login'))

    return render_template("home.html",title=title, name=session['name'],items=items)

@app.route("/uploadProfileImg", methods=['GET','POST'])
def uploadProfileImg():
    if request.method == 'POST':
        return "OK you got it"


@app.route("/admin/thrash")
def adminThrash():
    title = 'THRASH'
    return render_template("admin-trash.html",title=title)
    
@app.route("/myfiles")
def myFiles():
    positions = getAll("position")
    title = 'MY FILES'
    return render_template("myFiles.html",title=title, positions = positions)

@app.route("/admin/comments")
def adminComments():
    title = 'COMMENTS'
    return render_template("admin-comments.html",title=title)


@app.route("/admin/password")
def adminPassword():
    title = 'Password'
    return render_template("admin-password.html",title=title)

@app.route("/dashboard")
#ALSO SAVE AN EVENT IN CASE FOR NOTIFICATIONS

def dashboard():
    positions = getAll("position")
    title = 'DASHBOARD'
    return render_template("dashboard.html",title=title, positions = positions)

@app.route("/pinned")
def pinned():
    title = 'PINNED'
    return render_template("pinned.html",title=title)
@app.route("/shared")
def shared():
    title = 'PINNED'
    return render_template("shared.html",title=title)

@app.route("/deleted")
def deleted():
    title = 'DELETE'
    return render_template("delete.html",title=title)

@app.route("/settings")
def settings():
    title = 'SETTINGS'
    return render_template("settings.html",title=title)

@app.route("/UpdateUser", methods=['GET','POST'])
def updateUser():
    if request.method == "POST":
        id = request.form.get("id")
        email = request.form.get('Email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phoneNumber = request.form.get('PhoneNumber')
        position = request.form.get('Position')
    result = updateUserDB(id, email, firstName, lastName, phoneNumber, position)
    if result == True:
        return redirect(url_for("admin"))

@app.route("/admin/users" , methods=['GET','POST'])
def admin(result = ''):
    title = 'ADMIN'
    positions = getAll("position")
    if request.method == 'POST':
        if(request.form.get("delete")):
            deleteID = request.form.get("delete")
            result = deleteUserDB(deleteID)
            users = getAllUsers()
            return render_template("admin.html",title=title, positions=positions, result = result, users= users)
        email = request.form.get('Email')
        password = request.form.get('Password')
        repeatPass = request.form.get('RepeatPass')
        firstName = request.form.get('FirstName')
        lastName = request.form.get('LastName')
        phoneNumber = request.form.get('PhoneNumber')
        position = request.form.get('Position')
        result = registerNewUser(email, password, repeatPass, firstName, lastName, phoneNumber, position)
        users = getAllUsers()
        return render_template("admin.html",title=title, positions=positions, result = result, users= users)

    users = getAllUsers()
    return render_template("admin.html",title=title, positions=positions, result = result, users= users)


@app.route("/admin/files")
def adminFiles():
    title = 'FILES'
    return render_template("adminFiles.html",title=title)

@app.route("/profile/")
def profile():
    title = 'PROFILE'
    #Check if Sessions Exist
    if session['logged_in'] is False:
        return redirect(url_for('login'))

    result = getUserData(session['userID'])
    position = getPosition(result[0][6])
    positions = getAll("position")
    return render_template("profile.html",title=title, profile_details = result, position=position, positions = positions)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadfile", methods=['GET','POST'])
def uploadFile():
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
            
            lastID = saveFiletoDb(filename,filetype, filesize, file_content_type,uploaded_by, share_to_user, share_to_group,deadline, revision)
            # result = getFileDb(lastID[0][0])
            # data = '[{"id":"xPmqz3gBHy","type":"header","data":{"text":"PAUL IAN MASENDO","level":1}}]'
            print(lastID[0][0])
            return redirect(url_for('editor', id=lastID[0][0], ))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        print(file.filename)
        # filesize
        filename = str(session['userID']) + file.filename 
        # filesize = len(file.read())
        filesize = 1
        filetype = 'raw file'
        file_content_type = file.content_type
        share_to_group = request.form.get("Position")
        share_to_user = request.form.get("targetUser")
        deadline = request.form.get('Deadline')
        revision = 1
        uploaded_by = session['userID']
        lastID = saveFiletoDb(filename,filetype, filesize, file_content_type,uploaded_by, share_to_user, share_to_group,deadline, revision)

        file.save(os.path.join(app.root_path,app.config['UPLOAD_FOLDER'], filename))
        print(lastID[0][0])
        return redirect(url_for('file', id=lastID[0][0]))


    return render_template("fileupload.html", title=title)

@app.route('/uploads', methods=['GET', 'POST'])
def download(filename = "FILENAME.png"):
    uploads = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'])
    print(uploads)
    return send_from_directory(uploads, filename)


@app.route('/file/<id>')
def file(id):
    result = getFileDb(id)
    result = result[0]
    title = "File"
    if result[2] == 'block doc':
        return render_template("editor.html", title = title, result = result)
    

    if result[5] != session['userID']:
        return redirect(url_for("forbidden"))
    return render_template("file.html", title = title, result = result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/test123", methods=['GET', 'POST'])
def getEditorData():
    data = request.args.get('data')
    id = int(request.args.get('id'))
    print("DATA",data)
    print("ID", type(id))
    updateDocDB(id, data)
    
    return 'test'

@app.route("/forbidden")
def forbidden():
    return render_template("forbidden.html")

@app.route("/editor/<id>")
def editor(id):
    title = "FILE EDITOR"
    result = getFileDb(id)
    result = result[0]
    print(result)
    return render_template("editor.html", title = title, result= result)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


## https://www.youtube.com/watch?v=71EU8gnZqZQ