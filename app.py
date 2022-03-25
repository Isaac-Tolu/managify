from flask import Flask
from flask import request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return("<h1>This is a money management app.</h1>")

@app.route('/user/<name>')
def greet(name):
    return(f"<h1>Welcome back, {name}\nMake sure to catch up</h1>")

@app.route('/check')
def check_user_agent():
    return f"<h1>Your User Agent is {request.headers.get('User-Agent')}"

@app.route('/bad')
def bad():
    return '<h1>Bad Request</h1>', 400

@app.route('/redirect')
def redirect_func():
    return redirect('https://www.google.com/search?q=money')
