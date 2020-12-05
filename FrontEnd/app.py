from flask import render_template, redirect
from flask import Flask
from flask import request
from flask import url_for
from database import db
from models import Note as Note
from models import User as User
from models import Comment as Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

yourNotes = {
    0: {'title': 'First Note', 'text': 'This is my first note'},
    1: {'title': 'Second Note', 'text': 'This is my second note'},
    2: {'title': 'Third Note', 'text': 'This is my third note'}
}


@app.route("/")
def main():
    return redirect('/login')


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


@app.route("/notes")
def notes():
    # _notes = getNotes()
    return render_template('MainPage.html', notes=yourNotes)


@app.route('/note/<note_id>')
def viewNote(note_id):
    note_id = int(note_id)
    return render_template('viewNote.html', note=yourNotes.get(note_id))


@app.route('/addNote', methods=['POST'])
def addNote():

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        id = len(yourNotes)+1
        yourNotes[id] = {'title': title, 'text': text}

        return redirect(url_for('notes'))

# Edit note


@app.route('/note/edit/<note_id>')
def update_note(note_id):

    return render_template('MainPage.html', notes=yourNotes.get(note_id))


# Delete Note


@app.route('/note/delete/<note_id>', methods=['POST'])
def delete_note(note_id):

    yourNotes.pop(note_id)
    return render_template('viewNote.html')


if __name__ == "__main__":
    app.run()
