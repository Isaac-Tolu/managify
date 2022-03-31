from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

class SignInForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(),])
    email = StringField("Email:", validators=[DataRequired(), ])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=4, message="Password must be at least 4 characters long")])
    submit = SubmitField("Submit")

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route("/")
def index():
    return render_template("index.html", current_time=datetime.utcnow())

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        old_email = session.get("email")

        if old_name is not None and old_name != form.username.data:
            flash("Looks like you have changed your name!")
        if old_email is not None and old_email != form.email.data:
            flash("Looks like you've changed your email!")

        session["name"] = form.username.data
        session["email"] = form.email.data

        return redirect(url_for("signin"))
    return render_template("signin.html", form=form, name=session.get("name"))