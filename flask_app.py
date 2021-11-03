from enum import unique
from flask import Flask, render_template,request,json
from database import registerNewUser

app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        print(email)
        print(password)


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
        registerNewUser(email)



    return render_template('register.html')

@app.route("/forgotpassword")
def forgotpassword():
    return render_template('forgot-password.html')

@app.route("/test")
def test():
    dict={"data":{"test":"Bayside"}}
    return json.dumps(dict)


if __name__ == "__main__":
    app.run(debug=True)


## https://www.youtube.com/watch?v=71EU8gnZqZQ