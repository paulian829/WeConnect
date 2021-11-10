from enum import unique
from flask import Flask, render_template,request,json,redirect,url_for,session
from database import *

app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def login():

    session['logged_in'] = False
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        if (len(username) == 0 or len(password) == 0 ):
            result = "Error"
            return render_template('login.html',result = result)
        result = loginDB(username, password)
        if(result == "Error"):
            return render_template('login.html',result = result)

        session['logged_in'] = True
        session['userID'] = result[0][0]
        session['name'] = result[0][4]
        return redirect(url_for('home'))
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
        result = registerNewUser(username, email, password, repeatPass, name, phoneNumber, position)
        print(result)
        return render_template('register.html',result = result, positions = positions)
    else:
        return render_template('register.html',positions = positions)


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

@app.route("/admin")
def admin():
    title = 'ADMIN'
    return render_template("admin.html",title=title)

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