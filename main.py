from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from tabledef import *
import hashlib

app = Flask(__name__)
engine = create_engine('sqlite:///web.db', echo=True)
salt = "l0ld0ngz"

@app.route('/')
def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    pword = str(request.form['password'] + salt)
    salty = hashlib.md5(pword.encode())
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = salty.hexdigest()
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        return home()
    else:
        flash('Incorrect password or username')
        return home()
    

@app.route('/newuser')
def newuser():
	return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():

    pword = str(request.form['password'] + salt)
    salty = hashlib.md5(pword.encode())
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = salty.hexdigest()

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]))
    result = query.first()
    if result:
        flash('This user already exists')
        return newuser()
    else:
        user = User(POST_USERNAME, POST_PASSWORD)
        s.add(user)
        # commit the record the database
        s.commit()
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/user", methods=["POST"])
def add_user():

    Session = sessionmaker(bind=engine)
    s = Session()
   
    username = str(request.json['username'])
    password = str(request.json['password'])
    
    user = User(username, password)

    s.add(user)
    s.commit()

    return jsonify(user)


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)