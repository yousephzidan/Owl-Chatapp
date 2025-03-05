from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms import PasswordField 
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Login")

class Register(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Register")


app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = "secert_key" 
csrf = CSRFProtect(app)

@app.get("/")
def index_page():
    return render_template("index.html")

@app.get("/login")
def login_page():
    form = Login()

    return render_template("login.html", form=form)

@app.get("/register")
def register_page():
    form = Register()

    return render_template("register.html", form=form)
if "__main__" == __name__: 
    app.run(debug=True)
