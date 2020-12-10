from flask import render_template, redirect
from flask import Flask
from flask import request
from flask import url_for
from database import db
from models import Note as Note
from models import User as User
from models import Comment as Comment

# set vairable "app" to flask
app = Flask(__name__)

# Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialzie database "db"
db.init_app(app)
with app.app_context():
    db.create_all()


# Homepage route
@app.route("/")
def main():
    return redirect('/login')


# Login page route
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']

        # fake login functionality
        if password != '' and username != '':
            return redirect('/notes')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')

# Register page route -- also contains password authentication


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        confirmPassword = request.form['Confirm']

        # fake login functionality
        if password == confirmPassword:
            return redirect('/notes')
        else:
            return redirect('/register')
    else:
        return render_template('register.html')


# Access to list of notes
@app.route("/notes")
def notes():
    # _notes = getNotes()
    a_user = db.session.query(User).filter_by(email=User.name)
    my_note = db.session.query(Note).all()
    return render_template('MainPage.html', notes=my_note)

# Access to indiviual notes with a unique note id


@app.route('/note/<note_id>')
def viewNote(note_id):
    a_user = db.session.query(User).filter_by(email=User.name)
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    return render_template('viewNote.html', note=my_note, user=a_user)


# User capibility to add notes -- saves notes to database "db"
@app.route('/addNote', methods=['GET', 'POST'])
def addNote():

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        from datetime import date
        today = date.today()
        today = today.strftime('%m-%d-%Y')
        new_record = Note(title, text, today)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('notes'))
    else:
        a_user = db.session.query(User).filter_by(email=User.name)
        return render_template('mainPage.html', user=a_user)


# Edit note and updating notes -- saving it to database "db"
@app.route('/note/edit/<note_id>', methods=['POST'])
def update_note(note_id):
    if request.method == 'POST':
        text = request.form['text']
        note = db.session.query(Note).filter_by(id=note_id).one()

        note.text = text

        db.session.add(note)
        db.session.commit()
    return redirect('/note/' + str(note.id))


# Delete Note -- updateing databse to reflect deletion
@app.route('/note/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()

    return redirect('/notes')


# start the application "app"
if __name__ == "__main__":
    app.run()
