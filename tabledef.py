from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_marshmallow import Marshmallow
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify


app = Flask(__name__)
engine = create_engine('sqlite:///web.db', echo=True)
Base = declarative_base()
ma = Marshmallow(app)
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'password')

 
# create tables
Base.metadata.create_all(engine)