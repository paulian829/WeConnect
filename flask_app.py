from enum import unique
from flask import Flask, render_template,request,json,redirect,url_for,session
from database import *

app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def login():

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
    return render_template('login.html')


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
    dict={"data":{"test":"Bayside"}}
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


@app.route("/dashboard")
def dashboard():
    title = 'DASHBOARD'
    return render_template("dashboard.html",title=title)

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

    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True, use_reloader=True)


## https://www.youtube.com/watch?v=71EU8gnZqZQ