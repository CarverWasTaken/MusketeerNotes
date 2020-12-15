from database import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from database import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
class Note(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    title = db.Column("title",db.String(200))
    text = db.Column("text",db.String(100))
    date = db.Column("date",db.String(50))
    #comments = db.relationship("comment",backref="note",cascade="all,delete-orphan",lazy = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

    def __init__(self,title,text,date,user_id):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id

class User(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column("name",db.String(200))
    password = db.Column("password",db.String(255),nullable=False)
    notes = db.relationship("Note",backref="user",lazy=True)

    #comments = db.relationship("comment",backref="note",lazy = True)

    def __init__(self,name,password):
        self.name = name
        self.password = password

class Comment(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    text = db.Column("text",db.String(100))
    date = db.Column("date",db.String(50))
    parent_id = Column("parent_id", ForeignKey('note.id'))

    def __init__(self,text,date,parent_id):
        self.text = text
        self.date = date
        self.parent_id = parent_id
