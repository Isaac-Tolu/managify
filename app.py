import os
from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    transactions = db.relationship('Transaction', backref='user', lazy="dynamic")

    def __repr__(self):
        return "<User %r>" % self.username

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Numeric)
    reason = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Transaction %r>" % self.reason

class SignInForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(),])
    email = StringField("Email:", validators=[DataRequired(), ])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=4, message="Password must be at least 4 characters long")])
    submit = SubmitField("Submit")

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Transaction=Transaction)

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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            current_user = User(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data
            )
            db.session.add(current_user)
            db.session.commit()
            
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.username.data

        # old_name = session.get("name")
        # old_email = session.get("email")

        # if old_name is not None and old_name != form.username.data:
        #     flash("Looks like you have changed your name!")
        # if old_email is not None and old_email != form.email.data:
        #     flash("Looks like you've changed your email!")

        # session["name"] = form.username.data
        # session["email"] = form.email.data

        return redirect(url_for("signin"))
    return render_template("signin.html", form=form, name=session.get("name"),
                            known=session.get("known")
                            )