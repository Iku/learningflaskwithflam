from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
import hashlib
engine = create_engine('sqlite:///web.db', echo=True)
 
app = Flask(__name__)

salt = "l0ld0ngz"

@app.route('/')
def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    pword = str(request.form['username'] + salt)
    salty = hashlib.md5(pword.encode())
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = salty.hexdigest()
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/newuser')
def newuser():
	return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():

    pword = str(request.form['username'] + salt)
    salty = hashlib.md5(pword.encode())
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = salty.hexdigest()

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]))
    result = query.first()
    if result:
        flash('This user already exists')
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

@app.route('/injectweed')
def injectweed():
	return render_template("injectweed.html")



if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)