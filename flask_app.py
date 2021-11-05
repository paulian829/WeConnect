from enum import unique
from flask import Flask, render_template,request,json,redirect,url_for
#from database import registerNewUser

app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        print(email)
        print(password)
        return redirect(url_for('home'))


    return render_template('login.html')

@app.route("/register", methods=['GET','POST'])
def register():

    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        repeatPass = request.form.get('RepeatPass')
        name = request.form.get('Name')
        phoneNumber = request.form.get('PhoneNumber')
        position = request.form.get('Position')
        #registerNewUser(email)

    return render_template('register.html')

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
    return render_template("home.html",title=title)

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
    return render_template("profile.html",title=title)


if __name__ == "__main__":
    app.run(debug=True)


## https://www.youtube.com/watch?v=71EU8gnZqZQ