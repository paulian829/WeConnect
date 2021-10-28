from enum import unique
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisseacretkey'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    date_created = db.column(db.DateTime)


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder":"email"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder":"password"})

    submit = SubmitField("Login")

@app.route("/",methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html',form=form)


@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/forgotpassword")
def forgotpassword():
    return render_template('forgot-password.html')


if __name__ == "__main__":
    app.run(debug=True)