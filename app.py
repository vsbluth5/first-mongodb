import os
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from datetime import datetime
from dotenv import load_dotenv

# -- Initialization section --
app = Flask(__name__)

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"},
        {"event":"D-Day Anniversary", "date":"2019-06-06"}
    ]

# name of database
app.config['MONGO_DBNAME'] = 'firstDB'
# first load environment variables in .env
load_dotenv()

# then store environment variables with new names
USER = os.getenv("MONGO_USERNAME")
PASS = os.getenv("MONGO_PASSWORD")

# URI of database
#app.config['MONGO_URI'] = 'mongodb+srv://admin:TcKWGXMtarv9Mkjl@cluster0-vmzkd.mongodb.net/test?retryWrites=true&w=majority'
app.config['MONGO_URI'] = 'mongodb+srv://'+USER+':'+PASS+'@cluster0-vmzkd.mongodb.net/firstDB?retryWrites=true&w=majority'

#A secret key for the session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#session is defined in flask. This is one of its predefined fields.
#session['username'] = "VirginiaB"

mongo = PyMongo(app)

# INDEX
@app.route('/')
@app.route('/index')
def index():
    collection = mongo.db.events
    eventsDB = collection.find({})
    return render_template('index.html', events = eventsDB)


# CONNECT TO DB, ADD DATA
@app.route('/add')

def add():
    user = mongo.db.users
    user.insert({'name':'Julio'})
    return 'Added User!'

@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']

        events = mongo.db.events
        #print(events)
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return getAccess()

#Displays all events on another webpage
@app.route('/events')
def findEvents():
    collection = mongo.db.events
    #eventsDB = collection.find({})
    #eventsDB = collection.find_one({'name': 'CS1'})    #not iterable, only one
    #eventsDB = collection.find({'event' : 'Homework'})
    #eventsDB = collection.find({}).limit(10)     #limits results to 10
    #eventsDB = collection.find({}).sort('date', DESCENDING).limit(5)     #comboDB
    eventsDB = collection.find({}).sort('date', -1)  #1 means ascending, -1 is descending

    return render_template('events.html', events = eventsDB)

@app.route('/event/<eventID>')
def event(eventID):
    print('hi')
    print(eventID)
    collection = mongo.db.events
    event = collection.find_one({'_id' : ObjectId(eventID)})
    return render_template('event.html', event = event)
    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        
        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists! Try logging in.'
    return render_template('signup.html')
    
@app.route('/page1', methods=['GET'])
def getAccess():
    collection = mongo.db.events
    eventsDB = collection.find({})
    return render_template('page1.html', events = eventsDB)

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    print (login_user)
    if login_user:
        print(login_user['password'])
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            #collection = mongo.db.events
            #eventsDB = collection.find({})
            #return render_template('page1.html', events = eventsDB)
            return getAccess()
            

    return 'Invalid username/password combination'
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')