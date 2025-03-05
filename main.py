from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms import PasswordField 
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from flask_login import (
        LoginManager,
        UserMixin,
        login_user,
        login_required,
        logout_user,
        current_user,
        )


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ysf:pass@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


@app.get("/")
def index_page():
    return render_template("index.html")

@app.get("/login")
def login_page():
    form = Login()

    return render_template("login.html", form=form)

@app.post("/login")
def process_login_data():
    form = Login()


    if form.validate_on_submit():
        email = form.data.get("email")
        password = form.data.get("password")
        
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return render_template("home.html")

    flash("Wrong credentials! Please try again!")
    return redirect(url_for("login"))



@app.get("/register")
def register_page():
    form = Register()

    return render_template("register.html", form=form)

@app.post("/register")
def process_registeration_data():

    form = Register()
    
    if form.validate_on_submit():
        name = form.data.get("name")
        email = form.data.get("email")  
        password = form.data.get("password")  

        user = User.query.filter_by(email=email).first()

        if user:
            flash("User Already Exists! Log in instead")
            return redirect(url_for("login_page"))
        
        new_user = User(name=name, email=email,password=password)
        db.session.add(new_user)
        db.session.commit()

        print(User.query.all())

        flash("Registeration Sucessful!")
        return redirect(url_for("login_page"))

    flash("Registeration Failed!")
    return redirect(url_for("register_page"))
    
if "__main__" == __name__: 

    with app.app_context():
        db.create_all()
    app.run(debug=True)
