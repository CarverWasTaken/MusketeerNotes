from database import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
class Note(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    title = db.Column("title",db.String(200))
    text = db.Column("text",db.String(100))
    date = db.Column("date",db.String(50))
    children = relationship("Child")

    def __init__(self,title,text,date):
        self.title = title
        self.text = text
        self.date = date

class User(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column("name",db.String(200))
    email = db.Column("email",db.String(200))

    def __init__(self,name,email):
        self.name = name
        self.email = email

class Comment(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    text = db.Column("text",db.String(100))
    date = db.Column("date",db.String(50))
    parent_id = Column("parent_id", ForeignKey('parent.id'))
